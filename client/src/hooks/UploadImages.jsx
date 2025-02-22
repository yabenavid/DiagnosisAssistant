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
 * Función recursiva para extraer imágenes de subcarpetas (máximo 10 imágenes)
 */
export const extractImagesDiagnostic = async (dirHandle, zip, maxImages) => {
    let count = 0;
    let images = []; // Array para almacenar archivos de imagen

    for await (const entry of dirHandle.values()) {
        if (count >= maxImages) break; // Si ya hay 10 imágenes, salir del bucle

        if (entry.kind === "file") {
            const file = await entry.getFile();
            if (file.type.startsWith("image/")) {
                const fileData = await file.arrayBuffer();
                zip.file(file.name, fileData);
                images.push({ name: file.name, url: URL.createObjectURL(file) }); // Guardar la imagen en el array
                count++;
            }
        } else if (entry.kind === "directory") {
            const subImages = await extractImages(entry, zip, maxImages - count); // Extraer imágenes de subcarpetas
            images = images.concat(subImages);
            count += subImages.length;
        }
    }

    return { count, images };
};

/**
 * Función para seleccionar una carpeta y extraer imágenes (máximo 10 imágenes)
 */
export const handleSelectFolderDiagnostic = async (setFolderName, setImageCount, setZipFile, setImageList) => {
    const MAX_IMAGES = 10;

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

        //Mostrar alerta si se superó el límite de 10 imágenes
        if (count > MAX_IMAGES) {
            alert("La carpeta seleccionada tiene más de 10 imágenes. Solo se tomarán las primeras 10.");
        }

        setImageCount(count);
        setImageList(images); // Guardar las imágenes en el estado

        // Comprimir la carpeta a ZIP
        const zipBlob = await zip.generateAsync({ type: "blob" });
        setZipFile(zipBlob);
    } catch (error) {
        console.error("Error al seleccionar la carpeta:", error);
    }
};
