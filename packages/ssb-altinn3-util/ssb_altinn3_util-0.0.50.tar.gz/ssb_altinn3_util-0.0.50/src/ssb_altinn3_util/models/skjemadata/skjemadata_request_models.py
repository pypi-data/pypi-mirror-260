from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


class PeriodeRequestModel(BaseModel):
    id: Optional[int] = None
    skjema_id: int
    periode_type: Optional[str] = None
    periode_nr: Optional[int] = None
    periode_aar: Optional[int] = None
    periode_dato: Optional[date] = None
    delreg_nr: Optional[int] = None
    enhet_type: Optional[str] = None
    vis_oppgavebyrde: Optional[str] = "N"
    vis_brukeropplevelse: Optional[str] = "N"
    altinn_tilgjengelig: Optional[date] = None
    altinn_svarfrist: Optional[date] = None
    endret_av: str


class UtsendingRequestModel(BaseModel):
    id: Optional[int] = None
    periode_id: int
    utsendingstype: str
    pulje: Optional[int] = None
    trigger: Optional[str] = "Manuell"
    test: Optional[bool] = False
    utsendingsmal: Optional[str] = None
    utsendingsmal_versjon: Optional[int] = None
    altinn_uts_tidspunkt: Optional[datetime] = None
    altinn_tilgjengelig: Optional[datetime] = None
    altinn_svarfrist: Optional[date] = None
    endret_av: str


class SkjemaRequestModel(BaseModel):
    id: Optional[int] = None
    ra_nummer: str
    versjon: int
    undersokelse_nr: str
    datamodell: Optional[str] = None
    beskrivelse: Optional[str] = None
    navn_nb: Optional[str] = None
    navn_nn: Optional[str] = None
    navn_en: Optional[str] = None
    infoside: Optional[str] = None
    eier: Optional[str] = None
    kun_sky: Optional[str] = "N"
    gyldig_fra: date
    gyldig_til: Optional[date] = None
    endret_av: str
    prefill_template_type: Optional[str] = None
    prefill_template_version: Optional[int] = None


class SkjemaPrefillMetaRequestModel(BaseModel):
    id: Optional[int] = None
    skjema_id: int
    navn: str
    sti: Optional[str] = None
    rekkefolge: int
    type: Optional[str] = "ORDINAR"
    antall: Optional[int] = None
    kontroll: Optional[str] = "INGEN"
    stat_navn: Optional[str] = None
    kommentar: Optional[str] = None
    endret_av: str
