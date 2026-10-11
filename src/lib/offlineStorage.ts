import { set, get, del, clear } from 'idb-keyval';
import { Song } from '../types';

export const saveAudioOffline = async (song: Song) => {
   const url = song.audioUrl || song.coverUrl; // Fallback to coverUrl for mock download if no audio
   try {
       const res = await fetch(url);
       const blob = await res.blob();
       await set(`song-${song.id}`, blob);
       
       // Also try to cache the image in Cache API for true offline visual
       if (song.coverUrl && 'caches' in window) {
           const cache = await caches.open('app-images');
           await cache.add(song.coverUrl);
       }
   } catch (e) {
       console.error("Failed to download blob for", song.id);
   }
}

export const getOfflineAudioUrl = async (id: string): Promise<string | null> => {
   const blob = await get(`song-${id}`);
   if (blob) {
       return URL.createObjectURL(blob);
   }
   return null;
}

export const deleteAudioOffline = async (id: string) => {
   await del(`song-${id}`);
}

export const clearAllOfflineAudio = async () => {
   await clear();
}

export const getAvailableStorage = async () => {
   if (navigator.storage && navigator.storage.estimate) {
       return await navigator.storage.estimate();
   }
   return null;
}
