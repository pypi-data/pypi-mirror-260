from pih.tools import j, js, jp
from pih.consts import EMAIL_SPLITTER


class ADDRESSES:
    SITE_NAME: str = "pacifichosp"
    SITE_ADDRESS: str = jp((SITE_NAME, "com"))
    EMAIL_SERVER_ADDRESS: str = jp(("mail", SITE_ADDRESS))
    RECEPTION_NAME: str = "reception"
    ADD_EMAIL_NAME: str = "add_email"
    RECEPTION_LOGIN: str = jp((RECEPTION_NAME, SITE_NAME))

    WIKI_SITE_NAME: str = "wiki"
    WIKI_SITE_ADDRESS: str = WIKI_SITE_NAME
    OMS_SITE_NAME: str = "oms"
    OMS_SITE_ADDRESS: str = OMS_SITE_NAME
    API_SITE_ADDRESS: str = jp(("api", SITE_ADDRESS))
    BITRIX_SITE_URL: str = "bitrix.cmrt.ru"


class EMAIL_COLLECTION:
    MAIL_RU_NAME: str = "mail.ru"
    MAIL_RU_DAEMON: str = jp(("mailer-daemon@corp", MAIL_RU_NAME))
    MAIL_RU_IMAP_SERVER: str = jp(("imap", MAIL_RU_NAME))

    NAS: str = j(("nas", ADDRESSES.SITE_ADDRESS), EMAIL_SPLITTER)
    IT: str = j(("it", ADDRESSES.SITE_ADDRESS), EMAIL_SPLITTER)
    RECEPTION: str = j(
        (ADDRESSES.RECEPTION_NAME, ADDRESSES.SITE_ADDRESS), EMAIL_SPLITTER
    )
    ADD_EMAIL: str = j(
        (ADDRESSES.ADD_EMAIL_NAME, ADDRESSES.SITE_ADDRESS), EMAIL_SPLITTER
    )
    EXTERNAL: str = js(("mail.", ADDRESSES.SITE_NAME, EMAIL_SPLITTER, MAIL_RU_NAME))

    EXTERNAL_SERVER: str = MAIL_RU_IMAP_SERVER
