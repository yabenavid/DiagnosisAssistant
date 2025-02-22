import i18next from "i18next";
import I18NextHttpBackend from "i18next-http-backend";
import { initReactI18next } from "react-i18next";

i18next
    .use(I18NextHttpBackend) // Permite cargar archivos JSON desde "public"
    .use(initReactI18next)
    .init({
        lng: "es", // Idioma por defecto
        fallbackLng: "en", // Si falta una traducción, usa inglés
        ns: ["errors", "common", "forms", "auth"], // Nombres de archivos JSON en "public/locales"
        defaultNS: "common", // Si no se especifica namespace, usa "common"
        backend: {
            loadPath: "/locales/{{lng}}/{{ns}}.json" // Ruta para cargar JSONs
        },
        interpolation: { escapeValue: false }
    });

export default i18next;
