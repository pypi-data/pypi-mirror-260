from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional


class PeriodeResponseModel(BaseModel):
    id: int
    skjema_id: int
    periode_type: Optional[str] = None
    periode_nr: Optional[int] = None
    periode_aar: Optional[int] = None
    periode_dato: Optional[date] = None
    delreg_nr: Optional[int] = None
    enhet_type: Optional[str] = None
    vis_oppgavebyrde: str
    vis_brukeropplevelse: str
    altinn_tilgjengelig: Optional[date] = None
    altinn_svarfrist: Optional[date] = None
    endret_dato: datetime
    endret_av: str


class UtsendingResponseModel(BaseModel):
    id: int
    periode_id: int
    utsendingstype: str
    pulje: Optional[int] = None
    trigger: str
    test: bool
    utsendingsmal: Optional[str] = None
    utsendingsmal_versjon: Optional[int] = None
    altinn_uts_tidspunkt: Optional[datetime] = None
    altinn_tilgjengelig: Optional[datetime] = None
    altinn_svarfrist: Optional[date] = None
    endret_dato: datetime
    endret_av: str


class SkjemaResponseModel(BaseModel):
    id: int
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
    kun_sky: str
    gyldig_fra: date
    gyldig_til: Optional[date] = None
    endret_dato: datetime
    endret_av: str
    prefill_template_type: Optional[str] = None
    prefill_template_version: Optional[int] = None

    # perioder: Optional[List[PeriodeResponseModel]]


class SkjemaPrefillMetaResponseModel(BaseModel):
    id: int
    skjema_id: int
    navn: str
    sti: Optional[str] = None
    rekkefolge: int
    type: str
    antall: Optional[int] = None
    kontroll: Optional[str] = None
    stat_navn: Optional[str] = None
    kommentar: Optional[str] = None
    endret_dato: datetime
    endret_av: str
