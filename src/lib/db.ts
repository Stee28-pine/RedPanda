export function initDB() {
  return new Promise<IDBDatabase>((resolve, reject) => {
    const request = indexedDB.open('media-downloads', 1);
    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);
    request.onupgradeneeded = (e) => {
      const db = (e.target as IDBOpenDBRequest).result;
      if (!db.objectStoreNames.contains('assets')) {
        db.createObjectStore('assets', { keyPath: 'id' });
      }
    };
  });
}

export async function saveAssetToDB(id: string, metadata: any, blobUrl?: string) {
  const db = await initDB();
  return new Promise<void>((resolve, reject) => {
    const tx = db.transaction('assets', 'readwrite');
    const store = tx.objectStore('assets');
    const request = store.put({ id, metadata, blobUrl, timestamp: Date.now() });
    request.onsuccess = () => resolve();
    request.onerror = () => reject(request.error);
  });
}

export async function getAssetFromDB(id: string) {
  const db = await initDB();
  return new Promise<any>((resolve, reject) => {
    const tx = db.transaction('assets', 'readonly');
    const store = tx.objectStore('assets');
    const request = store.get(id);
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

export async function getAllAssetsFromDB() {
  const db = await initDB();
  return new Promise<any[]>((resolve, reject) => {
    const tx = db.transaction('assets', 'readonly');
    const store = tx.objectStore('assets');
    const request = store.getAll();
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}
