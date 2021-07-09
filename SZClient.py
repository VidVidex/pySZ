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
        vrste_ovir_response = self.zeep_client.service.Vrste_ovir(self.username, self.password)

        vrste_ovir = []
        for ovira in vrste_ovir_response:
            vrste_ovir.append({
                'id': ovira[0].text,
                'naziv': ovira[1].text
            })

        return vrste_ovir

    def zamude(self) -> list[dict]:
        zamude_response = self.zeep_client.service.Zamude(self.username, self.password)

        zamude = []
        for zamuda in zamude_response:
            zamude.append({
                'st_postaje': zamuda[0].text,
                'postaja': zamuda[1].text,
                'relacija': zamuda[2].text,
                'vlak': zamuda[3].text,
                'cas': zamuda[4].text,
                'vrsta': zamuda[5].text,
                'cas_eng': zamuda[6].text
            })

        return zamude

    def ovire(self, ang=False, arhiv=False) -> list[dict]:

        if ang and arhiv:
            ovire_response = self.zeep_client.service.Arhiv_ovir_ang(self.username, self.password)
        elif ang and not arhiv:
            ovire_response = self.zeep_client.service.Ovire_ang(self.username, self.password)
        elif not ang and arhiv:
            ovire_response = self.zeep_client.service.Arhiv_ovir(self.username, self.password)
        else:
            ovire_response = self.zeep_client.service.Ovire(self.username, self.password)

        ovire = []
        for ovira in ovire_response:
            ovire.append({
                'naslov': ovira[0].text,
                'cas': ovira[1].text,
                'lokacija': ovira[2].text,
                'relacija': ovira[3].text,
                'opis': ovira[4].text,
                'vrsta': ovira[5].text,
                'id_vrste': ovira[6].text,
                'id_ovire': ovira[7].text
            })

        return ovire

    def postaje(self) -> list[dict]:
        postaje_response = self.zeep_client.service.Postaje(self.username, self.password)

        postaje = []
        for postaja in postaje_response:
            postaje.append({
                'st': postaja[0].text,
                'naziv': postaja[1].text,
                'geo_sirina': self.__parse_float(postaja[2].text),
                'geo_dolzina': self.__parse_float(postaja[3].text)
            })

        return postaje

    def ovirani_vlaki(self, kolo=False) -> list[dict]:

        if kolo:
            ovirani_vlaki_response = self.zeep_client.service.Ovirani_vlaki_kolo(self.username, self.password)
        else:
            ovirani_vlaki_response = self.zeep_client.service.Ovirani_vlaki(self.username, self.password)

        ovirani_vlaki = []
        for vlak in ovirani_vlaki_response:
            ovirani_vlaki.append({
                'st_vlaka': vlak[0].text,
                'st_postaje': vlak[1].text,
                'datum_od': vlak[2].text,
                'datum_do': vlak[3].text,
                'od': vlak[4].text,
                'do': vlak[5].text,
                'st_ovire': vlak[6].text
            })

        return ovirani_vlaki

    def wifi(self, arhiv=False) -> list[dict]:

        if arhiv:
            # Začasno ne vrača arhiva ker je zgleda zelo velik in request traja predolgo
            return []
            # wifi_response = self.zeep_client.service.WiFi_arh(self.username, self.password)
        else:
            wifi_response = self.zeep_client.service.WiFi(self.username, self.password)

        wifi = []
        for w in wifi_response:
            wifi.append({
                'datum': w[0].text,
                'vlak': w[1].text,
                'garnitura': w[2].text
            })

        return wifi



