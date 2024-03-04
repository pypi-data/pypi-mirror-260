import requests
import urllib3
import base64

urllib3.disable_warnings()


class ZyxelApi:


    def __init__(self, ip, username, password):
        """
        Initialize the class with the ip of the router, username and password that you use to login to the https or http page for 
        your Zyxel EMG3525 router
        """
        self.ip = ip
        self.username = username
        self.password = base64.b64encode(bytes(password, 'utf-8')).decode()
        self.session = requests.session()
        self.session.headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'If-Modified-Since': 'Thu, 01 Jun 1970 00:00:00 GMT',
    'Origin': f'https://{self.ip}',
    'Pragma': 'no-cache',
    'Referer':f'https://{self.ip}/login',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
        self.cookies = {}
        self.data = '{"Input_Account":"%s","Input_Passwd":"%s","currLang":"en","RememberPassword":0,"SHA512_password":false}' % (self.username, self.password)


    def set_cookie(self):
        """
        

        Returns
        -------
        Only sets the cookie for the class, needs to be called before access is granted to the device

        """
        try:
            response = self.session.post(f"https://{self.ip}/UserLogin", data=self.data, verify=False)
            if response.ok:
                self.cookies = self.session.cookies.get_dict()
            else:
                print("Error setting cookig please check the username and password that was used")
        except:
            print("Error connecting to device check if device is switched on an reachble via https")
    
    def get_cardPageStatus(self):
        """
        

        Returns
        -------
        Dictionary with the following keys:
            'result', 'ReplyMsg', 'ReplyMsgMultiLang', 'Object'
            The Object key in the dictionary is a list containing one dictionary with the following keys:
                card_res['Object'][0].keys()
                Out: dict_keys(['WanLanInfo', 'DeviceInfo', 'LanPortInfo', 'WiFiInfo', 
                                    'Dhcp4SerPoolInfo', 'WWANStatsInfo', 'LanInfo', 
                                    'DslChannelInfo', 'OptIntfInfo', 'GponStatsInfo', 
                                    'partctlNum', 'GuestSSIDEnable', 'RdpaWanType', 
                                    'WanRate_RX', 'WanRate_TX'])
                
                So to get the current WanLanInfo you can use card_res['Object'][0]['WanLanInfo'] 
            Returns None if cookie could not be set
        """
        if self.cookies == {}:
            self.set_cookie()
            if self.cookies == {}:
                """Failed to set the cookie"""
                return None
        params = {
    'oid': 'cardpage_status',
}
        response = self.session.get(f'https://{self.ip}/cgi-bin/DAL', params=params, cookies=self.cookies, verify=False)
        if response.ok:
            return response.json()
        else:
            return {"responseCode": response.reason}
        
    def get_lanHosts(self):
        """
        

        Returns
        -------
        Dictionary with the following keys:
            'result', 'ReplyMsg', 'ReplyMsgMultiLang', 'Object'
            The Object key in the dictionary is a list containing one dictionary with the following keys:
                lanhosts['Object'][0].keys()
                Out: dict_keys(['wanInfo', 'lanhosts', 'STBVendorID'])
                
                So to get the current WanLanInfo you can use card_res['Object'][0]['WanLanInfo'] 
                Lanhosts has the has the following keys:
                    lanhosts['Object'][0]['lanhosts'][0].keys()
                    Out: dict_keys(['Alias', 'PhysAddress', 'IPAddress', 
                                    'IPAddress6', 'IPLinkLocalAddress6', 
                                    'AddressSource', 'DHCPClient', 'LeaseTimeRemaining', 
                                    'AssociatedDevice', 'Layer1Interface', 'Layer3Interface', 
                                    'VendorClassID', 'ClientID', 'UserClassID', 'HostName', 
                                    'Active', 'X_ZYXEL_DeleteLease', 'X_ZYXEL_ConnectionType', 
                                    'X_ZYXEL_ConnectedAP', 'X_ZYXEL_HostType', 'X_ZYXEL_CapabilityType', 
                                    'X_ZYXEL_PhyRate', 'X_ZYXEL_WiFiStatus', 'X_ZYXEL_SignalStrength', 
                                    'X_ZYXEL_SNR', 'X_ZYXEL_RSSI', 'X_ZYXEL_SoftwareVersion', 'X_ZYXEL_LastUpdate', 
                                    'X_ZYXEL_Address6Source', 'X_ZYXEL_DHCP6Client', 'X_ZYXEL_BytesSent', 'X_ZYXEL_BytesReceived', 
                                    'X_ZYXEL_OperatingStandard', 'X_ZYXEL_LastDataDownlinkRate', 'X_ZYXEL_LastDataUplinkRate', 
                                    'IPv4AddressNumberOfEntries', 'IPv6AddressNumberOfEntries', 'ClientDuid', 
                                    'ExpireTime', 'SupportedFrequencyBands', 'WiFiname', 'DeviceIcon', 
                                    'Internet_Blocking_Enable', 'DeviceName', 'curHostName', 'dhcp4PoolExist', 
                                    'dhcp4PoolIid', 'dhcp4StaticAddrExist', 'dhcp4StaticAddrIid', 'dhcp4StaticAddrEnable', 
                                    'dhcp4StaticAddr', 'dhcp4StaticAddrNum', 'dhcp4StaticAddrUsedByOtherHost', 
                                    'staticIP', 'icon'])
                Returns None if cookie could not be set
        """
        if self.cookies == {}:
            self.set_cookie()
            if self.cookies == {}:
                """Failed to set the cookie"""
                return None
        params = {
    'oid': 'lanhosts',
}
        response = self.session.get(f'https://{self.ip}/cgi-bin/DAL', params=params, cookies=self.cookies, verify=False)
        if response.ok:
            return response.json()
        else:
            return {"responseCode": response.reason}
        
    def get_trafficStatus(self):
        """
        

        Returns
        -------
        Dictionary with the following keys:
            'result', 'ReplyMsg', 'ReplyMsgMultiLang', 'Object'
            The Object key in the dictionary is a list containing one dictionary with the following keys:
                traffic['Object'][0].keys()
                Out[90]: dict_keys(['ipIface', 'ipIfaceSt', 'pppIface', 'pppIfaceSt', 'ethIface', 'ethIfaceSt', 
                                    'bridgingPT', 'bridgingStatus', 'wifiSsid', 
                                    'wifiRadio', 'hosts', 'changeIconName'])
            Returns None if cookie could not be set
        """
        if self.cookies == {}:
            self.set_cookie()
            if self.cookies == {}:
                """Failed to set the cookie"""
                return None
        params = {
    'oid': 'Traffic_Status',
}
        response = self.session.get(f'https://{self.ip}/cgi-bin/DAL', params=params, cookies=self.cookies, verify=False)
        if response.ok:
            return response.json()
        else:
            return {"responseCode": response.reason}
        

    def get_log(self):
        """
        

        Returns
        -------
        List with one Dictionary with the following keys:
            logs[0].keys()
            Out: dict_keys(['Ret', 'Oid', 'Iid', 'result'])
           To view all log messages use you can use logs[0]['result'] if you saved this result in a logs variable.
        """
        if self.cookies == {}:
            self.set_cookie()
        
        response = self.session.get(f'https://{self.ip}/cgi-bin/Log?action=GET_LOG&oid=RDM_OID_LOG_CLASSIFY&iid=[1,0,0,0,0,0]', cookies=self.cookies, verify=False)
        if response.ok:
            return response.json()
        else:
            return {"responseCode": response.reason}
