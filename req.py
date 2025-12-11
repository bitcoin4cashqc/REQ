from typing import Optional, Any, Dict
import cloudscraper
from .types import REQSearchResponse, SearchOptions, ListeEntreprises


BASE_URL = "https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_20A_PIU_RechEntMob_PC/ServiceCommunicationInterne.asmx"
REFERER_URL = "https://www.registreentreprises.gouv.qc.ca/RQAnonymeGR/GR/GR03/GR03A2_20A_PIU_RechEntMob_PC/index.html"


class REQ:
    """Client for the Quebec Business Register (Registre des entreprises du Québec) API"""

    def __init__(self):
        self.session_key: Optional[str] = None
        self.cookie: Optional[str] = None
        self._scraper = cloudscraper.create_scraper()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self._scraper:
            self._scraper.close()

    def get_neq(self, neq: str) -> Dict[str, Any]:
        """
        Get enterprise information by NEQ number

        Args:
            neq: The NEQ (Numéro d'entreprise du Québec) to look up

        Returns:
            Enterprise information
        """
        criterias = {"Id": neq}
        return self._do_request("POST", "/ObtenirEtatsRensEntreprise", criterias)

    def search(self, options: SearchOptions) -> REQSearchResponse:
        """
        Search for enterprises

        Args:
            options: Search options including keywords, domain, type, etc.

        Returns:
            Search response with list of enterprises
        """
        criterias = {
            "Domaine": options.domain,
            "Etendue": options.etendue,
            "PageCourante": options.page or 0,
            "Texte": options.keywords,
            "Type": options.type,
            "UtilisateurAccepteConditionsUtilisation": True,
        }
        result = self._do_request("POST", "/ObtenirListeEntreprises", criterias)

        # Convert the response to REQSearchResponse object
        if result is None:
            raise Exception("Received None from API request")

        # Handle case where ListeEntreprises is None (e.g., search term too general)
        entreprises_list = result.get("ListeEntreprises") or []
        liste_entreprises = [
            ListeEntreprises(**entreprise) for entreprise in entreprises_list
        ]

        return REQSearchResponse(
            PageCourante=result.get("PageCourante", 0),
            NombrePages=result.get("NombrePages", 0),
            ListeEntreprises=liste_entreprises,
            TotalEnregistrements=result.get("TotalEnregistrements", 0),
            CleSession=result.get("CleSession", ""),
            TypeResultat=result.get("TypeResultat", ""),
            Message=result.get("Message", ""),
        )

    def _new_request(self, method: str, url: str, criterias: Dict[str, Any]) -> tuple[str, Dict[str, str], Dict]:
        """
        Create a new request

        Args:
            method: HTTP method
            url: URL path
            criterias: Request criteria

        Returns:
            Tuple of (full_url, headers, body)
        """
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
            "Content-Type": "application/json; charset=UTF-8",
            "Origin": "https://www.registreentreprises.gouv.qc.ca",
            "Referer": REFERER_URL,
            "X-Requested-With": "XMLHttpRequest",
        }

        if self.cookie:
            headers["Cookie"] = self.cookie

        body = {
            "critere": {
                "UtilisateurAccepteConditionsUtilisation": True,
                "CleSession": self.session_key,
            }
        }

        body["critere"].update(criterias)

        full_url = BASE_URL + url

        return full_url, headers, body

    def _do_request(self, method: str, url: str, criterias: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute an HTTP request

        Args:
            method: HTTP method
            url: URL path
            criterias: Request criteria

        Returns:
            Response data
        """
        full_url, headers, body = self._new_request(method, url, criterias)

        response = self._scraper.request(method, full_url, headers=headers, json=body)

        # Check if the response is successful
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text[:500]}")

        # Extract cookie if present
        if "Set-Cookie" in response.headers:
            self.cookie = response.headers["Set-Cookie"].split(" ")[0]

        # Try to parse JSON response
        try:
            response_data = response.json()
        except Exception as e:
            raise Exception(f"Failed to parse JSON response: {e}\nResponse: {response.text[:500]}")

        # Extract session key from response
        if "d" in response_data and "CleSession" in response_data["d"]:
            self.session_key = response_data["d"]["CleSession"]

        return response_data.get("d", response_data)

    def close(self):
        """Close the HTTP session"""
        if self._scraper:
            self._scraper.close()
