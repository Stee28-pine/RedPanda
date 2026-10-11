import { Song } from '../types';

export interface SongContext {
  language: 'punjabi' | 'hindi' | 'english' | 'kpop' | 'other';
  mood: 'romantic' | 'sad' | 'upbeat' | 'chill' | 'hiphop' | 'rock' | 'general';
  genre: string;
  artist: string;
}

const PUNJABI_ARTISTS = [
  'ap dhillon', 'gurinder gill', 'diljit dosanjh', 'karan aujla', 'shubh',
  'sidhu moosewala', 'sidhu moose wala', 'b praak', 'harrdy sandhu',
  'amrit maan', 'jas manak', 'jass manak', 'guru randhawa', 'imran khan',
  'bohemia', 'mickey singh', 'prophec', 'prabh deep', 'sukhe', 'mankirt aulakh',
  'ammy virk', 'parmish verma', 'jordan sandhu', 'kaka'
];

const PUNJABI_KEYWORDS = [
  'punjabi', 'bhangra', 'munde', 'jatt', 'kudi', 'kinni', 'pyaar', 'gallan',
  'gaddi', 'aujla', 'dosanjh', 'challa', 'tauba', 'patola', 'mitran', 'so high',
  'excuses', 'brown munde', 'insane', 'born to shine', 'cheques', 'baller', 'no love'
];

const HINDI_ARTISTS = [
  'arijit singh', 'atif aslam', 'sonu nigam', 'jubin nautiyal', 'roop kumar rathod',
  'tochi raina', 'alka yagnik', 'shreya ghoshal', 'mohit chauhan', 'kk', 'k.k.',
  'pritam', 'sachin-jigar', 'vishal-shekhar', 'ar rahman', 'a.r. rahman',
  'mithoon', 'amit trivedi', 'rahat fateh ali khan', 'darshan raval', 'neha kakkar',
  'armaan malik', 'stebin ben', 'vishal mishra', 'king', 'badshah', 'sunidhi chauhan',
  'kumar sanu', 'udit narayan', 'shankar mahadevan', 'asees kaur', 'papon', 'shilpa rao'
];

const HINDI_KEYWORDS = [
  'indian love', 'bollywood', 'hindi', 'sufi', 'ghazal', 'tum hi ho', 'kesariya',
  'raataan lambiyan', 'apna bana le', 'shayad', 'channa mereya', 'kabira',
  'agar tum saath ho', 'kal ho naa ho', 'dil diyan gallan', 'tujh mein rab',
  'tera ban jaunga', 'pasoori', 'gerua', 'hawayein', 'tum se hi', 'jeena jeena',
  'khairiyat', 'ishq', 'mohabbat', 'deewana', 'aashiqui', 'dhadkan', 'sanam'
];

const KPOP_ARTISTS = [
  'bts', 'blackpink', 'jungkook', 'fifty fifty', 'newjeans', 'twice', 'stray kids',
  'le sserafim', 'aespa', 'ive', 'seventeen', 'joji', 'utada hikaru', 'txt', 'exo',
  'red velvet', 'iu', 'taeyeon', 'enhypen', 'nct'
];

const ROMANTIC_KEYWORDS = [
  'love', 'romantic', 'romance', 'lover', 'die for you', 'snooze', 'tum hi ho',
  'kesariya', 'raataan lambiyan', 'apna bana le', 'shayad', 'dil diyan gallan',
  'tujh mein rab', 'tera ban jaunga', 'pasoori', 'gerua', 'hawayein', 'tum se hi',
  'kinni kinni', 'softly', 'with you', 'enchanted', 'perfect', 'photograph',
  'thinking out loud', 'as it was', 'birds of a feather', 'cruel summer', 'heart'
];

const SAD_KEYWORDS = [
  'sad', 'heartbreak', 'cry', 'alone', 'tears', 'broken', 'channa mereya',
  'kabira', 'kal ho naa ho', 'agar tum saath ho', 'glimpse of us',
  'slow dancing in the dark', 'save your tears', 'khairiyat', 'losing grip'
];

const UPBEAT_KEYWORDS = [
  'dance', 'party', 'dynamite', 'butter', 'levitating', 'espresso', 'starboy',
  'blinding lights', 'brown munde', 'born to shine', 'excuses', '295', 'baller',
  'elevated', 'how you like that', 'pink venom', 'super shy', 'bad guy', 'believer',
  'synth-pop', 'k-pop', 'pop', 'bhangra'
];

const HIPHOP_ARTISTS_KEYWORDS = [
  'kendrick lamar', 'drake', 'travis scott', 'post malone', 'eminem', 'j. cole',
  '21 savage', 'future', 'metro boomin', 'hip-hop', 'rap', 'humble', 'not like us',
  'gods plan', 'sicko mode', 'sunflower'
];

/**
 * Automatically inspects a song's metadata, title, artist, and genre
 * to determine its language, listening mood, and context.
 */
export function detectSongContext(song: Song): SongContext {
  const titleLow = (song.title || '').toLowerCase();
  const artistLow = (song.artist || '').toLowerCase();
  const genreLow = (song.genre || '').toLowerCase();
  const albumLow = (song.album || '').toLowerCase();
  const combined = `${titleLow} ${artistLow} ${genreLow} ${albumLow}`;

  // 1. Language detection
  let language: SongContext['language'] = 'english';

  if (song.language) {
    const l = song.language.toLowerCase();
    if (l.includes('punjabi')) language = 'punjabi';
    else if (l.includes('hindi') || l.includes('bollywood')) language = 'hindi';
    else if (l.includes('kpop') || l.includes('korean') || l.includes('jpop')) language = 'kpop';
    else if (l.includes('english')) language = 'english';
  } else {
    const isPunjabiArtist = PUNJABI_ARTISTS.some(a => artistLow.includes(a));
    const hasPunjabiKeywords = PUNJABI_KEYWORDS.some(k => combined.includes(k));

    const isHindiArtist = HINDI_ARTISTS.some(a => artistLow.includes(a));
    const hasHindiKeywords = HINDI_KEYWORDS.some(k => combined.includes(k));

    const isKpopArtist = KPOP_ARTISTS.some(a => artistLow.includes(a));
    const isKpopGenre = genreLow.includes('k-pop') || genreLow.includes('j-pop');

    if (isPunjabiArtist || hasPunjabiKeywords) {
      language = 'punjabi';
    } else if (isHindiArtist || hasHindiKeywords) {
      language = 'hindi';
    } else if (isKpopArtist || isKpopGenre) {
      language = 'kpop';
    } else {
      language = 'english';
    }
  }

  // 2. Mood & Category detection
  let mood: SongContext['mood'] = 'general';

  if (song.mood) {
    const m = song.mood.toLowerCase();
    if (m.includes('romantic') || m.includes('love')) mood = 'romantic';
    else if (m.includes('sad')) mood = 'sad';
    else if (m.includes('upbeat') || m.includes('party')) mood = 'upbeat';
    else if (m.includes('hiphop') || m.includes('rap')) mood = 'hiphop';
    else if (m.includes('chill') || m.includes('acoustic')) mood = 'chill';
    else if (m.includes('rock')) mood = 'rock';
  } else {
    if (HIPHOP_ARTISTS_KEYWORDS.some(k => combined.includes(k))) {
      mood = 'hiphop';
    } else if (SAD_KEYWORDS.some(k => combined.includes(k))) {
      mood = 'sad';
    } else if (ROMANTIC_KEYWORDS.some(k => combined.includes(k)) || genreLow.includes('love')) {
      mood = 'romantic';
    } else if (genreLow.includes('rock') || genreLow.includes('metal')) {
      mood = 'rock';
    } else if (genreLow.includes('acoustic') || artistLow.includes('tissot')) {
      mood = 'chill';
    } else if (UPBEAT_KEYWORDS.some(k => combined.includes(k))) {
      mood = 'upbeat';
    } else {
      mood = 'general';
    }
  }

  return {
    language,
    mood,
    genre: song.genre || 'Music',
    artist: song.artist,
  };
}

/**
 * Scores candidate songs for recommendation based on context matching.
 * Guarantees language consistency (Punjabi -> Punjabi, Hindi romantic -> Hindi romantic, English love -> English love),
 * mood coherence, artist variety (no 3 songs in a row by same artist), and strictly honors "Don't Recommend" list.
 */
export function scoreCandidateSong(
  candidate: Song,
  targetContext: SongContext,
  options: {
    lastArtist?: string;
    recentHistoryIds?: string[];
    notRecommendedIds: string[];
    currentQueueIds: string[];
  }
): number {
  // STRICT RULE: If marked "Don't Recommend", NEVER recommend under any circumstance!
  if (options.notRecommendedIds.includes(candidate.id)) {
    return -Infinity;
  }

  // STRICT RULE: If already in current active queue, do not duplicate
  if (options.currentQueueIds.includes(candidate.id)) {
    return -Infinity;
  }

  const candidateContext = detectSongContext(candidate);
  let score = 50; // Base score

  // 1. Language Match (Highest Weight: 100 points)
  if (candidateContext.language === targetContext.language) {
    score += 100;
  } else {
    // Heavy cross-language penalty so Punjabi follows Punjabi, Hindi follows Hindi, etc.
    score -= 120;
  }

  // 2. Mood & Listening Context Match (High Weight: 60 points)
  if (candidateContext.mood === targetContext.mood) {
    score += 60;
  } else if (
    (targetContext.mood === 'romantic' && candidateContext.mood === 'sad') ||
    (targetContext.mood === 'sad' && candidateContext.mood === 'romantic')
  ) {
    // Romantic and emotional/sad can cross smoothly with a slight penalty
    score += 25;
  } else if (
    (targetContext.mood === 'upbeat' && candidateContext.mood === 'hiphop') ||
    (targetContext.mood === 'hiphop' && candidateContext.mood === 'upbeat')
  ) {
    score += 30;
  } else {
    score -= 20;
  }

  // 3. Genre Match
  if (candidateContext.genre && targetContext.genre && candidateContext.genre.toLowerCase() === targetContext.genre.toLowerCase()) {
    score += 25;
  }

  // 4. Artist Spacing & Variety (Keep variety, avoid excessive repetition)
  const isSameArtist = candidate.artist.toLowerCase() === targetContext.artist.toLowerCase();
  if (isSameArtist) {
    if (options.lastArtist && options.lastArtist.toLowerCase() === candidate.artist.toLowerCase()) {
      // Immediate repetition penalty for artist diversity
      score -= 30;
    } else {
      score += 15;
    }
  }

  // 5. Cooldown for recently played history
  if (options.recentHistoryIds && options.recentHistoryIds.includes(candidate.id)) {
    const idx = options.recentHistoryIds.indexOf(candidate.id);
    // If played very recently (within 5 tracks), strong penalty
    if (idx < 5) {
      score -= 50;
    } else {
      score -= 15;
    }
  }

  // 6. Micro-jitter (+/- 3 points) to ensure variety across long listening sessions
  score += (Math.random() * 6 - 3);

  return score;
}

/**
 * Selects the best matching songs from the catalog to replenish the infinite queue.
 */
export function getSmartRecommendations(
  currentSong: Song,
  catalog: Song[],
  options: {
    count?: number;
    notRecommendedIds: string[];
    currentQueueIds: string[];
    recentHistoryIds?: string[];
  }
): Song[] {
  const targetContext = detectSongContext(currentSong);
  const count = options.count || 8;

  const validCandidates = catalog.filter(s => 
    s.id !== currentSong.id &&
    !options.notRecommendedIds.includes(s.id) &&
    !options.currentQueueIds.includes(s.id)
  );

  if (validCandidates.length === 0) {
    // If every candidate was already queued or filtered, recycle candidates that aren't blocked
    const recyclable = catalog.filter(s => 
      s.id !== currentSong.id && 
      !options.notRecommendedIds.includes(s.id)
    );
    return recyclable.slice(0, count);
  }

  const scored = validCandidates.map(candidate => ({
    song: candidate,
    score: scoreCandidateSong(candidate, targetContext, {
      lastArtist: currentSong.artist,
      recentHistoryIds: options.recentHistoryIds || [],
      notRecommendedIds: options.notRecommendedIds,
      currentQueueIds: options.currentQueueIds,
    })
  }));

  // Sort descending by match score
  scored.sort((a, b) => b.score - a.score);

  return scored.slice(0, count).map(item => item.song);
}

/**
 * Checks if the current queue needs replenishment and appends matching tracks.
 * Infinite playback ensures there are always at least `minBuffer` upcoming tracks.
 */
export function replenishInfiniteQueue(
  currentSong: Song | null,
  queue: Song[],
  catalog: Song[],
  notRecommendedIds: string[],
  recentHistoryIds: string[] = [],
  minBuffer: number = 5,
  batchSize: number = 8
): { replenishedQueue: Song[]; addedSongs: Song[] } {
  if (!currentSong) {
    return { replenishedQueue: queue, addedSongs: [] };
  }

  const currentIdx = queue.findIndex(s => s.id === currentSong.id);
  const upcomingCount = currentIdx !== -1 ? queue.length - 1 - currentIdx : queue.length;

  if (upcomingCount >= minBuffer) {
    return { replenishedQueue: queue, addedSongs: [] };
  }

  const currentQueueIds = queue.map(s => s.id);
  const needed = Math.max(batchSize, minBuffer - upcomingCount);

  const nextSongs = getSmartRecommendations(currentSong, catalog, {
    count: needed,
    notRecommendedIds,
    currentQueueIds,
    recentHistoryIds,
  });

  if (nextSongs.length === 0) {
    return { replenishedQueue: queue, addedSongs: [] };
  }

  return {
    replenishedQueue: [...queue, ...nextSongs],
    addedSongs: nextSongs,
  };
}

// In-memory cache for resolved YouTube video IDs to eliminate loading delays
const resolvedYtCache: Record<string, string> = {};

export function getCachedVideoId(songId: string): string | null {
  return resolvedYtCache[songId] || null;
}

export function cacheVideoId(songId: string, videoId: string): void {
  resolvedYtCache[songId] = videoId;
}

/**
 * Proactively pre-fetches and pre-resolves upcoming track video IDs in advance
 * so when the track transitions, playback starts seamlessly with 0s delay.
 */
export async function prefetchUpcomingTrack(
  nextSong: Song | null,
  onResolved?: (songId: string, videoId: string) => void
): Promise<string | null> {
  if (!nextSong) return null;
  if (nextSong.youtubeId) {
    cacheVideoId(nextSong.id, nextSong.youtubeId);
    return nextSong.youtubeId;
  }
  if (resolvedYtCache[nextSong.id]) {
    nextSong.youtubeId = resolvedYtCache[nextSong.id];
    return resolvedYtCache[nextSong.id];
  }

  try {
    const res = await fetch(`/api/youtube-search?q=${encodeURIComponent(nextSong.title + ' ' + nextSong.artist)}`);
    const data = await res.json();
    if (data?.videoId) {
      cacheVideoId(nextSong.id, data.videoId);
      nextSong.youtubeId = data.videoId;
      onResolved?.(nextSong.id, data.videoId);
      return data.videoId;
    }
  } catch (err) {
    console.debug('Prefetch upcoming track error (non-fatal):', err);
  }
  return null;
}
