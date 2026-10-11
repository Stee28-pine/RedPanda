export interface Song {
  id: string;
  title: string;
  artist: string;
  album: string;
  duration: string;
  durationSeconds: number;
  coverUrl: string;
  audioUrl?: string;
  youtubeId?: string;
  isLiked?: boolean;
  genre?: string;
  language?: string;
  mood?: string;
  plays?: number;
  lyrics?: { time: number; text: string }[];
}

export interface Collection {
  id: string;
  type: 'album' | 'playlist' | 'mix';
  title: string;
  subtitle: string;
  description?: string;
  coverUrl: string;
  songs: Song[];
  year?: string;
  genre?: string;
}

export interface Bookmark {
  id: string;
  songId: string;
  timestamp: number;
  note: string;
  createdAt: number;
}
