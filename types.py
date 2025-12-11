from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ListeEntreprises:
    """Enterprise list item"""
    ID: str
    NumeroDossier: str
    Nom: str
    AdressePrimaire: str
    Statut: str
    DateChangementEtat: str
    StatutDuNom: str
    DateInitiale: str
    DateFinale: str


@dataclass
class REQSearchResponse:
    """Search response from the Quebec Business Register API"""
    PageCourante: int
    NombrePages: int
    ListeEntreprises: List[ListeEntreprises]
    TotalEnregistrements: int
    CleSession: str
    TypeResultat: str
    Message: str


@dataclass
class REQRequestOptions:
    """Request options for the Quebec Business Register API"""
    CleSession: Optional[str] = None
    Domaine: Optional[int] = None
    Etendue: Optional[int] = None
    Id: Optional[str] = None
    PageCourante: Optional[int] = None
    Texte: Optional[str] = None
    Type: Optional[int] = None
    UtilisateurAccepteConditionsUtilisation: Optional[bool] = None


@dataclass
class REQRequest:
    """Request structure"""
    critere: REQRequestOptions


@dataclass
class SearchOptions:
    """Search options for enterprise search"""
    keywords: str
    domain: Optional[int] = None
    type: Optional[int] = None
    etendue: Optional[int] = None
    page: Optional[int] = None
