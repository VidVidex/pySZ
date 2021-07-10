from typing import Union

from zeep import Client


class SZClient:
    username: str
    password: str
    wsdl_url: str = 'http://91.209.49.139/webse/se.asmx?WSDL'
    zeep_client: Client

    @staticmethod
    def __parse_float(f: str) -> Union[float, None]:
        if f is None:
            return None
        else:
            return float(f)

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

        self.zeep_client = Client(self.wsdl_url)

    def vrste_vlakov(self) -> list[str]:
        vrste_vlakov_response = self.zeep_client.service.Vrste_vlakov(self.username, self.password)
        return [vrsta.text for vrsta in vrste_vlakov_response]

    def vrste_ovir(self) -> list[dict]:
        return self.__parse(self.zeep_client.service.Vrste_ovir(self.username, self.password))

    def zamude(self) -> list[dict]:
        return self.__parse(self.zeep_client.service.Zamude(self.username, self.password))

    def ovire(self, ang=False, arhiv=False) -> list[dict]:

        if ang and arhiv:
            ovire_response = self.zeep_client.service.Arhiv_ovir_ang(self.username, self.password)
        elif ang and not arhiv:
            ovire_response = self.zeep_client.service.Ovire_ang(self.username, self.password)
        elif not ang and arhiv:
            ovire_response = self.zeep_client.service.Arhiv_ovir(self.username, self.password)
        else:
            ovire_response = self.zeep_client.service.Ovire(self.username, self.password)

        return self.__parse(ovire_response)

    def postaje(self) -> list[dict]:
        return self.__parse(self.zeep_client.service.Postaje(self.username, self.password))

    def ovirani_vlaki(self, kolo=False) -> list[dict]:

        if kolo:
            ovirani_vlaki_response = self.zeep_client.service.Ovirani_vlaki_kolo(self.username, self.password)
        else:
            ovirani_vlaki_response = self.zeep_client.service.Ovirani_vlaki(self.username, self.password)
        return self.__parse(ovirani_vlaki_response)

    def wifi(self, arhiv=False) -> list[dict]:

        if arhiv:
            wifi_response = self.zeep_client.service.WiFi_arh(self.username, self.password)
        else:
            wifi_response = self.zeep_client.service.WiFi(self.username, self.password)

        return self.__parse(wifi_response)

    @staticmethod
    def __parse(response):
        rezultat = []
        for x in response:
            test = {}
            for y in x:
                test.update({
                    y.tag: y.text
                })
            rezultat.append(test)

        return rezultat
