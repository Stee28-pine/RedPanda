export interface ProgressEntry {
  progress: number;
  timestamp: number;
}

export class SyncManager {
  static getLocalProgress(profileId: string): Record<string, ProgressEntry> {
    try {
      const data = localStorage.getItem(`sync_progress_${profileId}`);
      return data ? JSON.parse(data) : {};
    } catch {
      return {};
    }
  }

  static saveLocalProgress(profileId: string, id: string, progress: number) {
    const allProgress = this.getLocalProgress(profileId);
    allProgress[id] = { progress, timestamp: Date.now() };
    localStorage.setItem(`sync_progress_${profileId}`, JSON.stringify(allProgress));
  }

  // Simulate pushing to remote server and resolving conflicts
  static async syncWithRemote(profileId: string, localData: Record<string, ProgressEntry>) {
    console.log('[SyncManager] Starting sync for profile:', profileId);
    
    // Simulate remote data
    const remoteDataStr = localStorage.getItem(`remote_db_progress_${profileId}`);
    let remoteData: Record<string, ProgressEntry> = remoteDataStr ? JSON.parse(remoteDataStr) : {};

    // Conflict Resolution: Latest timestamp wins
    let resolvedData: Record<string, ProgressEntry> = { ...remoteData };
    let hasChanges = false;

    for (const [id, localEntry] of Object.entries(localData)) {
      const remoteEntry = remoteData[id];
      if (!remoteEntry || localEntry.timestamp > remoteEntry.timestamp) {
        resolvedData[id] = localEntry;
        hasChanges = true;
      }
    }

    if (hasChanges) {
       console.log('[SyncManager] Resolved conflicts, remote updated:', resolvedData);
       localStorage.setItem(`remote_db_progress_${profileId}`, JSON.stringify(resolvedData));
    }
    
    // Update local with resolved remote (if any other device updated it)
    localStorage.setItem(`sync_progress_${profileId}`, JSON.stringify(resolvedData));
    return resolvedData;
  }
}
