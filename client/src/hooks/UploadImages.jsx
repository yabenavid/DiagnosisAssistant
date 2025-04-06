import JSZip from "jszip";

/**
 * Función recursiva para extraer imágenes de subcarpetas
 * @param {FileSystemDirectoryHandle} dirHandle - Directorio seleccionado
 * @param {JSZip} zip - Instancia de JSZip para comprimir archivos
 * @returns {Promise<number>} - Número total de imágenes extraídas
 */
export const extractImages = async (dirHandle, zip) => {
    let count = 0; // Contador local de imágenes

    for await (const entry of dirHandle.values()) {
        if (entry.kind === "file") {
            const file = await entry.getFile();
            if (file.type.startsWith("image/")) {
                const fileData = await file.arrayBuffer();
                zip.file(file.name, fileData);
                count++; // Contar la imagen
            }
        } else if (entry.kind === "directory") {
            count += await extractImages(entry, zip); // Acumular imágenes de subcarpetas
        }
    }

    return count;
};

/**
 * Función para seleccionar una carpeta, extraer imágenes y generar un ZIP
 * @param {Function} setFolderName - Setter para el nombre de la carpeta
 * @param {Function} setImageCount - Setter para el número de imágenes
 * @param {Function} setZipFile - Setter para el archivo ZIP generado
 */
export const handleSelectFolder = async (setFolderName, setImageCount, setZipFile) => {
    try {
        if (!window.showDirectoryPicker) {
            alert("Tu navegador no soporta la selección de carpetas.");
            return;
        }

        const folderHandle = await window.showDirectoryPicker();
        setFolderName(folderHandle.name);

        const zip = new JSZip();
        const totalImages = await extractImages(folderHandle, zip);

        if (totalImages === 0) {
            alert("La carpeta no contiene imágenes. Selecciona otra carpeta.");
            return;
        }

        setImageCount(totalImages);

        // Comprimir la carpeta a ZIP
        const zipBlob = await zip.generateAsync({ type: "blob" });
        setZipFile(zipBlob);
    } catch (error) {
        console.error("Error al seleccionar la carpeta:", error);
    }
};


/**
 * Función para extraer imágenes del directorio principal (sin subdirectorios)
 * @param {FileSystemDirectoryHandle} dirHandle - Directorio seleccionado
 * @param {number} maxImages - Número máximo de imágenes a extraer
 * @returns {Promise<{count: number, images: Array}>} - Número de imágenes y lista de imágenes extraídas
 */
export const extractImagesDiagnostic = async (dirHandle, maxImages) => {
    let count = 0;
    let images = []; // Array para almacenar archivos de imagen

    for await (const entry of dirHandle.values()) {
        if (count >= maxImages) break; // Si ya hay el máximo de imágenes, salir del bucle

        if (entry.kind === "file") {
            const file = await entry.getFile();
            if (file.type.startsWith("image/")) {
                images.push({
                    name: file.name,
                    url: URL.createObjectURL(file), // Crear una URL para previsualizar la imagen
                    file: file, // Incluir el archivo para su posterior envío
                });
                count++;
            }
        }
    }
    console.log("Imágenes extraídas:", images);
    return { count, images };
};

/**
 * Función para seleccionar una carpeta y extraer imágenes (máximo 10 imágenes)
 */
export const handleSelectFolderDiagnostic = async (setFolderName, setImageCount, setImageList) => {
    const MAX_IMAGES = 3;

    try {
        if (!window.showDirectoryPicker) {
            alert("Tu navegador no soporta la selección de carpetas.");
            return;
        }

        const folderHandle = await window.showDirectoryPicker();
        setFolderName(folderHandle.name);

        const zip = new JSZip();
        const { count, images } = await extractImagesDiagnostic(folderHandle, zip, MAX_IMAGES);

        if (count === 0) {
            alert("La carpeta no contiene imágenes. Selecciona otra carpeta.");
            return;
        }

        //Mostrar alerta si se superó el límite de 3 imágenes
        if (count > MAX_IMAGES) {
            alert("La carpeta seleccionada tiene más de 3 imágenes. Solo se tomarán las primeras 3.");
        }

        setImageCount(count);
        setImageList(images); // Guardar las imágenes en el estado

    } catch (error) {
        console.error("Error al seleccionar la carpeta:", error);
    }
};
