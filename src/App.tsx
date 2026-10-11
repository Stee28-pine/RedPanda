import React, { useState, useEffect, useRef } from 'react';
import { Sidebar } from './components/Sidebar';
import { Player } from './components/Player';
import { TopBar } from './components/TopBar';
import { HomeView } from './components/HomeView';
import { PodcastsView } from './components/PodcastsView';
import { AlbumView } from './components/AlbumView';
import { SearchView } from './components/SearchView';
import { RightSidebar } from './components/RightSidebar';
import { Collection, Song } from './types';
import { SONGS } from './data';
import { motion, AnimatePresence } from 'motion/react';
import ReactPlayer from 'react-player';
import { useBookmarks } from './hooks/useBookmarks';
import { useSearch } from './hooks/useSearch';
import { usePlaylists } from './hooks/usePlaylists';
import { useListeningStats } from './hooks/useListeningStats';
import { StatsView } from './components/StatsView';
import { ShareModal } from './components/ShareModal';
import { HistoryView } from './components/HistoryView';
import { saveAudioOffline, deleteAudioOffline, clearAllOfflineAudio , getOfflineAudioUrl } from './lib/offlineStorage';

import { Check } from 'lucide-react';
import { SongContextMenu } from './components/SongContextMenu';
import { 
  detectSongContext, 
  getSmartRecommendations, 
  replenishInfiniteQueue, 
  prefetchUpcomingTrack,
  getCachedVideoId,
  cacheVideoId 
} from './lib/infiniteEngine';

export default function App() {
  const { playlists, createPlaylist, addSongToPlaylist, removeSongFromPlaylist, deletePlaylist, mergePlaylists } = usePlaylists();
  const { stats, recordPlay } = useListeningStats();
  const { bookmarks, addBookmark, removeBookmark } = useBookmarks();
  const [playlistModalSong, setPlaylistModalSong] = useState<Song | null>(null);
  const [showCreatePlaylistModal, setShowCreatePlaylistModal] = useState(false);
  const [newPlaylistName, setNewPlaylistName] = useState('');
  const [currentView, setCurrentView] = useState<'home' | 'album' | 'search' | 'podcasts' | 'history'>('home');
  const [activeCollection, setActiveCollection] = useState<Collection | null>(null);
  const [nowPlaying, setNowPlaying] = useState<Song | null>(null);

  const [isPlaying, setIsPlaying] = useState(false);
  const [showRightSidebar, setShowRightSidebar] = useState(false);
  const [showShortcuts, setShowShortcuts] = useState(false);
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(() => typeof window !== 'undefined' && window.innerWidth < 768);
  const [isLandscape, setIsLandscape] = useState(() => typeof window !== 'undefined' && window.matchMedia('(orientation: landscape)').matches);
  useEffect(() => {
    const mql = window.matchMedia('(orientation: landscape)');
    const onChange = (e: MediaQueryListEvent) => {
      setIsLandscape(e.matches);
      if (e.matches && window.innerWidth < 768) {
        setIsSidebarCollapsed(true);
      }
    };
    mql.addEventListener('change', onChange);
    return () => mql.removeEventListener('change', onChange);
  }, []);
  const [isScrolled, setIsScrolled] = useState(false);
  const [queue, setQueue] = useState<Song[]>([]);
  const [isShuffle, setIsShuffle] = useState(false);
  const [repeatMode, setRepeatMode] = useState<'none'|'all'|'one'>('none');
  
  const [searchQuery, setSearchQuery] = useState('');
  useEffect(() => {
    if (activeCollection?.type === 'playlist' && activeCollection.id !== 'liked-songs') {
      const updated = playlists.find(p => p.id === activeCollection.id);
      if (updated && updated.songs.length !== activeCollection.songs.length) {
        setActiveCollection(updated);
      }
    }
  }, [playlists, activeCollection?.id]);

  const { results: searchResults, isLoading: isSearchLoading } = useSearch(searchQuery);

  const [recentlyPlayed, setRecentlyPlayed] = useState<Song[]>(() => {
    try {
      const saved = localStorage.getItem('ais_recently_played');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('ais_recently_played', JSON.stringify(recentlyPlayed));
  }, [recentlyPlayed]);
  const [likedSongs, setLikedSongs] = useState<Song[]>([]);
  const [downloadedSongs, setDownloadedSongs] = useState<Song[]>([]);

  const [notRecommendedSongIds, setNotRecommendedSongIds] = useState<string[]>(() => {
    try {
      const saved = localStorage.getItem('ais_not_recommended_songs');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  useEffect(() => {
    localStorage.setItem('ais_not_recommended_songs', JSON.stringify(notRecommendedSongIds));
  }, [notRecommendedSongIds]);

  // Unified Catalog for Smart Recommendations & Infinite Playback
  const [catalogSongs, setCatalogSongs] = useState<Song[]>(SONGS);

  useEffect(() => {
    fetch("https://itunes.apple.com/us/rss/topsongs/limit=100/json")
      .then(res => res.json())
      .then(data => {
        if (data?.feed?.entry) {
          const fetched: Song[] = data.feed.entry.map((entry: any) => ({
            id: entry.id.attributes['im:id'],
            title: entry['im:name'].label,
            artist: entry['im:artist'].label,
            album: entry['im:collection']['im:name'].label,
            coverUrl: entry['im:image'][entry['im:image'].length - 1].label.replace(/170x170/g, '400x400'),
            genre: entry.category.attributes.label,
            duration: '0:30',
            durationSeconds: 30,
          }));
          setCatalogSongs(prev => {
            const existingIds = new Set(prev.map(s => s.id));
            const newSongs = fetched.filter(s => !existingIds.has(s.id));
            return [...prev, ...newSongs];
          });
        }
      })
      .catch(() => {});
  }, []);

  const [songContextMenu, setSongContextMenu] = useState<{
    x: number;
    y: number;
    song: Song;
    onRemoveFromPlaylist?: (s: Song) => void;
  } | null>(null);

  const handleOpenSongContextMenu = (
    e: React.MouseEvent | MouseEvent,
    song: Song,
    options?: { onRemoveFromPlaylist?: (s: Song) => void }
  ) => {
    e.preventDefault();
    e.stopPropagation();
    setSongContextMenu({
      x: e.clientX,
      y: e.clientY,
      song,
      onRemoveFromPlaylist: options?.onRemoveFromPlaylist,
    });
  };

  const [currentPlaybackTime, setCurrentPlaybackTime] = useState(0);
  const [toast, setToast] = useState<{ message: string } | null>(null);
  useEffect(() => {
    if (!toast) return;
    const timer = setTimeout(() => {
      setToast(null);
    }, 3000);
    return () => clearTimeout(timer);
  }, [toast]);
  const [shareItem, setShareItem] = useState<{ type: 'song' | 'album' | 'artist', id: string, name: string, data?: any } | null>(null);


  const playerRef = useRef<any>(null);
  const audioCtxRef = useRef<AudioContext | null>(null);
  const sourceNodeRef = useRef<MediaElementAudioSourceNode | null>(null);
  const gainNodeRef = useRef<GainNode | null>(null);
  const analyzerNodeRef = useRef<AnalyserNode | null>(null);
  const compressorNodeRef = useRef<DynamicsCompressorNode | null>(null);
  const [analyzerNode, setAnalyzerNode] = useState<AnalyserNode | null>(null);

  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [crossfadeVolume, setCrossfadeVolume] = useState(1);
  const [playbackRate, setPlaybackRate] = useState(1);
  const fadeOutIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const isCrossfading = useRef(false);
  const [isBuffering, setIsBuffering] = useState(false);
  const [youtubeId, setYoutubeId] = useState<string | null>(null);

  useEffect(() => {
    if (gainNodeRef.current) {
      // Smoothly transition volume
      gainNodeRef.current.gain.setTargetAtTime(volume * crossfadeVolume, audioCtxRef.current?.currentTime || 0, 0.1);
    }
  }, [volume, crossfadeVolume]);

  const [asyncBlobUrl, setAsyncBlobUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!nowPlaying) {
      setAsyncBlobUrl(null);
      setYoutubeId(null);
      return;
    }
    
    let isCurrent = true;

    const resolveUrl = async () => {
      // 1. Check Offline DB (async)
      const blobUrl = await getOfflineAudioUrl(nowPlaying.id);
      if (!isCurrent) return;
      if (blobUrl) {
         setAsyncBlobUrl(blobUrl);
         return;
      }
      
      // 2. Check instant in-memory cache first for zero latency
      let currentYtId = nowPlaying.youtubeId || getCachedVideoId(nowPlaying.id);
      if (!currentYtId) {
         setIsBuffering(true);
         try {
           const res = await fetch(`/api/youtube-search?q=${encodeURIComponent(nowPlaying.title + ' ' + nowPlaying.artist)}`);
           const data = await res.json();
           if (data.videoId) {
             currentYtId = data.videoId;
             nowPlaying.youtubeId = currentYtId;
             cacheVideoId(nowPlaying.id, currentYtId);
             if (data.thumbnail && (!nowPlaying.coverUrl || nowPlaying.coverUrl.includes('unsplash'))) {
               nowPlaying.coverUrl = data.thumbnail;
             }
           } else {
             // If unavailable, seamlessly continue to next suitable alternative
             if (isCurrent && isPlaying) {
               handleNext();
             }
           }
         } catch (err) {
           console.error("Failed to fetch YT ID", err);
           if (isCurrent && isPlaying) {
             handleNext();
           }
         } finally {
           if (isCurrent) setIsBuffering(false);
         }
      } else {
        cacheVideoId(nowPlaying.id, currentYtId);
      }
      
      if (!isCurrent) return;
      
      if (currentYtId) {
         setYoutubeId(currentYtId);
      }
    };

    resolveUrl();
    return () => { isCurrent = false; };
  }, [nowPlaying]);

  // Compute URL synchronously so it never drops to null between songs if we already have the youtubeId
  let nowPlayingUrl = "";
  if (nowPlaying) {
    const cachedYt = getCachedVideoId(nowPlaying.id);
    if (asyncBlobUrl && downloadedSongs.some(d => d.id === nowPlaying.id)) {
      nowPlayingUrl = asyncBlobUrl;
    } else if (nowPlaying.youtubeId) {
      nowPlayingUrl = `https://www.youtube.com/watch?v=${nowPlaying.youtubeId}`;
    } else if (cachedYt) {
      nowPlayingUrl = `https://www.youtube.com/watch?v=${cachedYt}`;
    } else if (youtubeId) {
      nowPlayingUrl = `https://www.youtube.com/watch?v=${youtubeId}`;
    } else if (nowPlaying.audioUrl) {
      nowPlayingUrl = nowPlaying.audioUrl;
    }
  }

  useEffect(() => {
    if (nowPlaying) {
       recordPlay(nowPlaying);
    }
  }, [nowPlaying?.id]);

  const currentPlaybackTimeRef = useRef(0);
  useEffect(() => {
    currentPlaybackTimeRef.current = currentPlaybackTime;
  }, [currentPlaybackTime]);

  // High-precision buffer-fill synchronization check
  useEffect(() => {
    let rafId: number;
    const syncLoop = () => {
      if (isPlaying && playerRef.current) {
        const internalTime = playerRef.current.getCurrentTime();
        if (internalTime !== null && internalTime !== undefined) {
          const drift = Math.abs(internalTime - currentPlaybackTimeRef.current);
          if (drift > 0.05) { // 50ms drift
             setCurrentPlaybackTime(internalTime);
          }
        }
      }
      rafId = requestAnimationFrame(syncLoop);
    };
    rafId = requestAnimationFrame(syncLoop);
    return () => cancelAnimationFrame(rafId);
  }, [isPlaying]);

  const handleProgress = (state: { playedSeconds: number }) => {
    // We let the RAF loop handle precise synchronization, but we keep this as a fallback
    // if the RAF loop misses an update for some reason.
    const drift = Math.abs(state.playedSeconds - currentPlaybackTimeRef.current);
    if (drift > 0.05) {
      setCurrentPlaybackTime(state.playedSeconds);
    }
  };

  const showToast = (message: string) => {
    setToast({ message });
    setTimeout(() => setToast(null), 3000);
  };

  const handleShare = (item: { type: 'song' | 'album' | 'artist', id: string, name: string, data?: any }) => {
    setShareItem(item);
  };
  const handleCopyLink = (url: string) => {
    if (typeof navigator !== 'undefined' && navigator.clipboard) {
      navigator.clipboard.writeText(url).catch(() => {});
    }
    showToast(`Link copied to clipboard`);
  };

  // Local persistence
  useEffect(() => {
    if (typeof window !== 'undefined') {
      try {
        const liked = localStorage.getItem('ais_liked_songs');
        if (liked) setLikedSongs(JSON.parse(liked));
        const downloaded = localStorage.getItem('ais_downloaded_songs');
        if (downloaded) setDownloadedSongs(JSON.parse(downloaded));
      } catch (e) {
        console.error("Failed to load state", e);
      }
    }
  }, []);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('ais_liked_songs', JSON.stringify(likedSongs));
    }
  }, [likedSongs]);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('ais_downloaded_songs', JSON.stringify(downloadedSongs));
    }
  }, [downloadedSongs]);

  const handleAddToQueue = (song: Song) => {
    if (nowPlaying?.id === song.id) {
       showToast(`Already playing`);
       return;
    }
    if (!nowPlaying) {
      setNowPlaying(song);
      setIsPlaying(true);
      setQueue([song]);
    } else {
      setQueue(prev => {
        const filtered = prev.filter(s => s.id !== song.id);
        return [...filtered, song];
      });
    }
    setShowRightSidebar(true);
    showToast(`Added to queue`);
  };

  const handlePlayNext = (song: Song) => {
    if (!nowPlaying) {
      setNowPlaying(song);
      setIsPlaying(true);
      setQueue([song]);
    } else {
      setQueue(prev => {
        const filtered = prev.filter(s => s.id !== song.id);
        const currentIndex = filtered.findIndex(s => s.id === nowPlaying.id);
        if (currentIndex === -1) {
          return [song, ...filtered];
        }
        const newQueue = [...filtered];
        newQueue.splice(currentIndex + 1, 0, song);
        return newQueue;
      });
    }
    showToast(`Will play next`);
  };

  const toggleLike = (song: Song) => {
    setLikedSongs(prev => {
      const exists = prev.some(s => s.id === song.id);
      let newLikedSongs;
      if (exists) {
        newLikedSongs = prev.filter(s => s.id !== song.id);
      } else {
        newLikedSongs = [...prev, song];
      }
      
      setActiveCollection(curr => {
        if (curr?.id === 'liked-songs') {
          return { ...curr, songs: newLikedSongs, subtitle: `${newLikedSongs.length} tracks` };
        }
        return curr;
      });
      
      return newLikedSongs;
    });
  };

  const toggleDownload = (song: Song) => {
    setDownloadedSongs(prev => {
      const exists = prev.some(s => s.id === song.id);
      if (exists) {
        deleteAudioOffline(song.id);
        showToast("Removed from downloads");
        return prev.filter(s => s.id !== song.id);
      }
      
      saveAudioOffline(song);
      showToast("Download started...");
      return [...prev, song];
    });
  };

  const handleNavigateToAlbum = (collection: Collection) => {
    setActiveCollection(collection);
    setCurrentView('album');
    setSearchQuery('');
  };


  const handleNavigateLikedSongs = () => {
    setActiveCollection({
      id: 'liked-songs',
      title: 'Liked Song',
      subtitle: '',
      type: 'playlist',
      coverUrl: 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&q=80',
      songs: likedSongs
    });
    setCurrentView('album');
    setSearchQuery('');
  };

  const handleNavigatePlaylist = (playlist: Collection) => {
    setActiveCollection(playlist);
    setCurrentView('album');
    setSearchQuery('');
  };

  const handleGenreClick = (genre: string) => {
    const genreSongs = SONGS.filter(s => s.genre === genre && !notRecommendedSongIds.includes(s.id));
    setActiveCollection({
      id: `genre-${genre}`,
      title: `${genre} Hits`,
      subtitle: 'Trending Now',
      type: 'playlist',
      coverUrl: genreSongs[0]?.coverUrl || 'https://images.unsplash.com/photo-1518609878373-06d740f60d8b?w=400&q=80',
      songs: genreSongs
    });
    setCurrentView('album');
    setSearchQuery('');
  };

  const handleNavigateHome = () => {
    setCurrentView('home');
    setSearchQuery('');
  };

  const handleSearchChange = (query: string) => {
    setSearchQuery(query);
    if (query.length > 0) {
      setCurrentView('search');
    }
  };

  const handleFadeOut = () => {
    if (!isPlaying) return;
    const duration = 3000;
    const steps = 30;
    const stepTime = duration / steps;
    let currentStep = 0;

    if (fadeOutIntervalRef.current) clearInterval(fadeOutIntervalRef.current);

    fadeOutIntervalRef.current = setInterval(() => {
      currentStep++;
      if (currentStep >= steps) {
        if (fadeOutIntervalRef.current) clearInterval(fadeOutIntervalRef.current);
        setIsPlaying(false);
        setCrossfadeVolume(1);
      } else {
        setCrossfadeVolume(1 - (currentStep / steps));
      }
    }, stepTime);
  };

    const handleSeekToTime = (time: number) => {
    if (playerRef.current) {
      playerRef.current.seekTo(time, 'seconds');
    }
    setCurrentPlaybackTime(time);
  };

  const handlePlaySong = (song: Song, context?: { songs: Song[] } | Collection) => {
    if (notRecommendedSongIds.includes(song.id)) {
      showToast(`Track is on your "Don't Recommend" list`);
      return;
    }

    setNowPlaying(song);
    setIsPlaying(true);
    
    setRecentlyPlayed(prev => {
      const isTarget = (s: Song) => s.id === song.id || (s.title === song.title && s.artist === song.artist);
      const filtered = prev.filter(s => !isTarget(s));
      return [song, ...filtered];
    });

    let baseQueue: Song[] = [song];
    if (context && 'songs' in context && context.songs.length > 0) {
      const idx = context.songs.findIndex(s => s.id === song.id);
      if (idx !== -1) {
        baseQueue = context.songs.slice(idx);
      } else {
        baseQueue = [song, ...context.songs.filter(s => s.id !== song.id)];
      }
    } else if (activeCollection && activeCollection.songs.length > 0) {
      const idx = activeCollection.songs.findIndex(s => s.id === song.id);
      if (idx !== -1) {
        baseQueue = activeCollection.songs.slice(idx);
      } else {
        baseQueue = [song, ...activeCollection.songs.filter(s => s.id !== song.id)];
      }
    }

    // Filter unrecommended songs from baseQueue
    baseQueue = baseQueue.filter(s => !notRecommendedSongIds.includes(s.id));

    // Automatically replenish infinite queue with matching context songs (language, mood, genre)
    const recentIds = recentlyPlayed.map(s => s.id);
    const { replenishedQueue } = replenishInfiniteQueue(
      song,
      baseQueue,
      catalogSongs,
      notRecommendedSongIds,
      recentIds,
      6,
      8
    );

    setQueue(replenishedQueue);
  };

  // Infinite Queue Auto-Replenisher:
  // Automatically monitors queue depth and continuously replenishes matching tracks
  // before the queue runs out, ensuring endless playback for hours.
  useEffect(() => {
    if (!nowPlaying || queue.length === 0) return;

    const currentIdx = queue.findIndex(s => s.id === nowPlaying.id);
    const upcomingCount = currentIdx !== -1 ? queue.length - 1 - currentIdx : queue.length;

    if (upcomingCount < 5) {
      const recentIds = recentlyPlayed.map(s => s.id);
      const { replenishedQueue, addedSongs } = replenishInfiniteQueue(
        nowPlaying,
        queue,
        catalogSongs,
        notRecommendedSongIds,
        recentIds,
        6,
        8
      );

      if (addedSongs.length > 0) {
        setQueue(replenishedQueue);
      }
    }
  }, [nowPlaying?.id, queue, catalogSongs, notRecommendedSongIds, recentlyPlayed]);

  // Seamless Experience: Proactively prepare upcoming songs in advance
  // Pre-resolves YouTube audio IDs in background to eliminate loading delay and silence
  useEffect(() => {
    if (!nowPlaying || queue.length === 0) return;
    const currentIdx = queue.findIndex(s => s.id === nowPlaying.id);
    if (currentIdx !== -1 && currentIdx < queue.length - 1) {
      const nextTrack = queue[currentIdx + 1];
      if (nextTrack) {
        prefetchUpcomingTrack(nextTrack, (songId, videoId) => {
          cacheVideoId(songId, videoId);
        });
      }
    }
  }, [nowPlaying?.id, queue]);

  // Automatic Recovery: If a track gets stuck buffering for > 7s while playing,
  // automatically advance to the next suitable alternative
  useEffect(() => {
    if (!isPlaying || !isBuffering || !nowPlaying) return;

    const watchdog = setTimeout(() => {
      if (isPlaying && isBuffering) {
        console.warn("Track buffering timeout, automatically continuing playback with next suitable track");
        handleNext();
      }
    }, 7000);

    return () => clearTimeout(watchdog);
  }, [isPlaying, isBuffering, nowPlaying?.id]);

  const handleReorderQueue = (newNextUp: Song[]) => {
    if (!nowPlaying) return;
    const currentIdx = queue.findIndex(s => s.id === nowPlaying.id);
    if (currentIdx === -1) return;
    
    const newQueue = [...queue];
    newQueue.splice(currentIdx + 1, newNextUp.length, ...newNextUp);
    setQueue(newQueue);
  };

  const transitionTrack = (action: () => void) => {
    if (isCrossfading.current || document.hidden) {
       setCrossfadeVolume(1);
       action();
       isCrossfading.current = false;
       return;
    }
    isCrossfading.current = true;
    
    const duration = 500;
    const steps = 10;
    const stepTime = duration / steps;
    let currentStep = 0;
    
    const fadeOut = setInterval(() => {
      currentStep++;
      if (currentStep >= steps || document.hidden) {
        clearInterval(fadeOut);
        setCrossfadeVolume(0);
        action();
        
        let inStep = 0;
        const fadeIn = setInterval(() => {
          inStep++;
          if (inStep >= steps || document.hidden) {
            clearInterval(fadeIn);
            setCrossfadeVolume(1);
            isCrossfading.current = false;
          } else {
            setCrossfadeVolume(inStep / steps);
          }
        }, stepTime);
      } else {
        setCrossfadeVolume(1 - (currentStep / steps));
      }
    }, stepTime);
  };

  const handleNext = () => {
    if (!nowPlaying) return;
    transitionTrack(() => {
      if (repeatMode === 'one') {
        setNowPlaying({ ...nowPlaying });
        setIsPlaying(true);
        if (playerRef.current) {
          playerRef.current.seekTo(0);
        }
        return;
      }

      const validQueue = queue.filter(s => !notRecommendedSongIds.includes(s.id));

      if (isShuffle && validQueue.length > 1) {
        const others = validQueue.filter(s => s.id !== nowPlaying.id);
        const randomChoice = others[Math.floor(Math.random() * others.length)];
        if (randomChoice) {
          setNowPlaying(randomChoice);
          setIsPlaying(true);
          return;
        }
      }

      const currentIdx = validQueue.findIndex(s => s.id === nowPlaying.id);
      if (currentIdx !== -1 && currentIdx < validQueue.length - 1) {
        const nextSong = validQueue[currentIdx + 1];
        setNowPlaying(nextSong);
        setIsPlaying(true);

        // Replenish in advance if approaching the end
        if (currentIdx + 2 >= validQueue.length) {
          const recentIds = recentlyPlayed.map(s => s.id);
          const { replenishedQueue } = replenishInfiniteQueue(
            nextSong,
            validQueue,
            catalogSongs,
            notRecommendedSongIds,
            recentIds,
            6,
            8
          );
          setQueue(replenishedQueue);
        }
      } else {
        // At the end of queue: Infinite playback automatically generates next matching batch!
        const recentIds = recentlyPlayed.map(s => s.id);
        const nextBatch = getSmartRecommendations(nowPlaying, catalogSongs, {
          count: 8,
          notRecommendedIds: notRecommendedSongIds,
          currentQueueIds: validQueue.map(s => s.id),
          recentHistoryIds: recentIds,
        });

        if (nextBatch.length > 0) {
          setQueue([...validQueue, ...nextBatch]);
          setNowPlaying(nextBatch[0]);
          setIsPlaying(true);
        } else if (repeatMode === 'all' && validQueue.length > 0) {
          setNowPlaying(validQueue[0]);
          setIsPlaying(true);
        }
      }
    });
  };

  const handlePrev = () => {
    if (!nowPlaying || queue.length === 0) return;
    transitionTrack(() => {
      if (isShuffle) {
        const randomIdx = Math.floor(Math.random() * queue.length);
        setNowPlaying(queue[randomIdx]);
        setIsPlaying(true);
        return;
      }
      const idx = queue.findIndex(s => s.id === nowPlaying.id);
      if (idx > 0) {
        setNowPlaying(queue[idx - 1]);
        setIsPlaying(true);
      } else if (repeatMode === 'all') {
        setNowPlaying(queue[queue.length - 1]);
        setIsPlaying(true);
      }
    });
  };

  const handleTrackPlaybackError = (error: any) => {
    console.warn("Track playback failed or unavailable, smoothly skipping to alternative track:", error);
    if (!nowPlaying) return;
    handleNext();
  };

  const handleDontRecommend = (song: Song) => {
    setNotRecommendedSongIds(prev => {
      if (prev.includes(song.id)) return prev;
      const updated = [...prev, song.id];
      localStorage.setItem('ais_not_recommended_songs', JSON.stringify(updated));
      return updated;
    });

    // Remove from active queue
    setQueue(prev => prev.filter(s => s.id !== song.id));

    // If currently playing, skip to next track
    if (nowPlaying?.id === song.id) {
      handleNext();
    }

    showToast(`"${song.title}" will not be recommended again`);
  };

  useEffect(() => {
    const handleDocumentContextMenu = (e: MouseEvent) => {
      const target = (e.target as HTMLElement)?.closest('[data-song-id]') as HTMLElement | null;
      if (target) {
        const songId = target.dataset.songId;
        if (songId) {
          const foundSong = SONGS.find(s => s.id === songId) || 
                            catalogSongs.find(s => s.id === songId) ||
                            queue.find(s => s.id === songId) || 
                            recentlyPlayed.find(s => s.id === songId) || 
                            searchResults.find(s => s.id === songId);
          if (foundSong) {
            e.preventDefault();
            setSongContextMenu({
              x: e.clientX,
              y: e.clientY,
              song: foundSong
            });
          }
        }
      }
    };
    document.addEventListener('contextmenu', handleDocumentContextMenu);
    return () => document.removeEventListener('contextmenu', handleDocumentContextMenu);
  }, [queue, recentlyPlayed, searchResults, catalogSongs]);


  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Don't trigger if user is typing in an input
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

      switch (e.code) {
        case 'Space':
          e.preventDefault();
          setIsPlaying(p => !p);
          break;
        case 'ArrowRight':
          e.preventDefault();
          if (playerRef.current) {
            const current = playerRef.current.getCurrentTime();
            const dur = playerRef.current.getDuration();
            if (dur) {
                playerRef.current.seekTo(Math.min(current + 10, dur), 'seconds');
            }
          }
          break;
        case 'ArrowLeft':
          e.preventDefault();
          if (playerRef.current) {
            const current = playerRef.current.getCurrentTime();
            playerRef.current.seekTo(Math.max(current - 10, 0), 'seconds');
          }
          break;
                case 'ArrowUp':
          e.preventDefault();
          setVolume(v => Math.min(v + 0.1, 1));
          break;
        case 'ArrowDown':
          e.preventDefault();
          setVolume(v => Math.max(v - 0.1, 0));
          break;
        case 'KeyN':
          e.preventDefault();
          handleNext();
          break;
        case 'KeyP':
          e.preventDefault();
          handlePrev();
          break;
        case 'Slash':
          if (e.shiftKey) {
            e.preventDefault();
            setShowShortcuts(prev => !prev);
          }
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleNext, handlePrev, nowPlaying, likedSongs, volume]);

  return (
    <div className="flex h-screen bg-[#f5f2ee] text-gray-900 font-sans overflow-hidden md:p-2 md:gap-2 select-none relative">
      {/* Toast Notification */}
      <AnimatePresence>
        {toast && (
          <motion.div
            initial={{ y: -50, opacity: 0, scale: 0.9 }}
            animate={{ y: 20, opacity: 1, scale: 1 }}
            exit={{ y: -50, opacity: 0, scale: 0.9 }}
            className="fixed top-6 left-1/2 -translate-x-1/2 z-[60] bg-white/80 backdrop-blur-xl border border-gray-200/50 shadow-lg rounded-full px-6 py-3 flex items-center gap-3 text-[14px] font-semibold text-gray-900"
          >
            <Check size={18} className="text-[#fe5f64]" />
            {toast.message}
          </motion.div>
        )}
      </AnimatePresence>

      {!isSidebarCollapsed && (
        <div 
          className="md:hidden fixed inset-0 z-30 bg-black/20 backdrop-blur-sm"
          onClick={() => setIsSidebarCollapsed(true)}
        />
      )}
      <div className={`fixed inset-y-0 left-0 z-40 p-0 md:p-0 transition-transform duration-300 md:relative md:transform-none ${isSidebarCollapsed ? '-translate-x-full md:translate-x-0' : 'translate-x-0'}`}>
        <Sidebar 
          onNavigateHome={handleNavigateHome} 
          onNavigatePodcasts={() => setCurrentView('podcasts')}          
          onNavigateHistory={() => setCurrentView('history')}
          currentView={currentView} 
          onNavigateLikedSongs={handleNavigateLikedSongs}
          likedSongs={likedSongs}
          activeCollectionId={activeCollection?.id}
          isCollapsed={isSidebarCollapsed}
          nowPlaying={nowPlaying}
          playlists={playlists}
          onDeletePlaylist={(id) => { deletePlaylist(id); if (activeCollection?.id === id) setActiveCollection(null); }}
          onMergePlaylist={(targetId, sourceId) => { mergePlaylists(targetId, sourceId); if (activeCollection?.id === sourceId) setActiveCollection(null); }}
          onNavigatePlaylist={(p) => {
             setActiveCollection(p);
             setCurrentView('album');
          }}
          onCreatePlaylist={() => setShowCreatePlaylistModal(true)}
        />
      </div>
      
      <main className="flex-1 flex flex-col bg-[#F9F9F9] md:rounded-2xl shadow-sm md:border md:border-gray-200 overflow-hidden relative">
        <TopBar 
          onBack={handleNavigateHome} 
          canGoBack={currentView !== 'home'} 
          searchQuery={searchQuery}
          onSearchChange={handleSearchChange}
          onSearchFocus={() => { if (currentView !== 'podcasts') setCurrentView('search'); }}
          onToggleSidebar={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        />
        
        <div className="flex-1 overflow-y-auto hide-scrollbar" onScroll={(e) => setIsScrolled(e.currentTarget.scrollTop > 60)}>
          <AnimatePresence mode="wait">
            {currentView === 'home' ? (
              <motion.div
                key="home"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="h-full"
              >
                <HomeView 
                  onCollectionClick={handleNavigateToAlbum}
                  playlists={playlists}
                  onPlaySong={handlePlaySong}
                  onGenreClick={handleGenreClick}
                  downloadedSongs={downloadedSongs}
                  recentlyPlayedHistory={recentlyPlayed}
                  likedSongs={likedSongs}
                  notRecommendedSongIds={notRecommendedSongIds}
                  onSongContextMenu={handleOpenSongContextMenu}
                  onDeletePlaylist={(id) => { deletePlaylist(id); setActiveCollection(null); }}
                  onMergePlaylist={(targetId, sourceId) => { mergePlaylists(targetId, sourceId); setActiveCollection(null); }}
                />
              </motion.div>
            ) : currentView === 'podcasts' ? (
              <motion.div
                key="podcasts"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="h-full"
              >
                <PodcastsView 
                  searchQuery={searchQuery}
                  onSearchChange={handleSearchChange}
                  onPlaySong={handlePlaySong} 
                  nowPlaying={nowPlaying} 
                  isPlaying={isPlaying} 
                  likedSongs={likedSongs}
                  onToggleLike={toggleLike}
                  currentTime={currentPlaybackTime}
                  bookmarks={bookmarks}
                  onAddBookmark={addBookmark}
                  onRemoveBookmark={removeBookmark}
                  onSeekToTime={handleSeekToTime}
                />
              </motion.div>
            ) : currentView === 'search' ? (
              <motion.div
                key="search"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="h-full"
              >
                <SearchView 
                  query={searchQuery} 
                  results={searchResults} 
                  isLoading={isSearchLoading} 
                  onPlaySong={handlePlaySong} 
                  nowPlaying={nowPlaying} 
                  isPlaying={isPlaying} 
                  likedSongs={likedSongs}
                  downloadedSongs={downloadedSongs}
                  onToggleLike={toggleLike}
                  onToggleDownload={toggleDownload}
                  onAddToQueue={handleAddToQueue}
                  onPlayNext={handlePlayNext}
                  onAddToPlaylist={setPlaylistModalSong}
                  onShare={handleShare}
                  onDontRecommend={handleDontRecommend}
                  onSongContextMenu={handleOpenSongContextMenu}
                  />
              </motion.div>
            ) : currentView === 'history' ? (
              <motion.div
                key="history"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="h-full"
              >
                <HistoryView 
                  recentlyPlayedHistory={recentlyPlayed}
                  onPlaySong={handlePlaySong}
                  onRemoveFromHistory={(song) => {
                    setRecentlyPlayed(prev => {
                      const isTarget = (s: Song) => 
                        (Boolean(s.id) && Boolean(song.id) && String(s.id) === String(song.id)) ||
                        (Boolean(s.title) && Boolean(song.title) && s.title.trim().toLowerCase() === song.title.trim().toLowerCase() &&
                         Boolean(s.artist) && Boolean(song.artist) && s.artist.trim().toLowerCase() === song.artist.trim().toLowerCase());
                      const updated = prev.filter(s => !isTarget(s));
                      try {
                        localStorage.setItem('ais_recently_played', JSON.stringify(updated));
                      } catch (err) {
                        console.error(err);
                      }
                      return updated;
                    });
                    showToast(`"${song.title}" deleted from history`);
                  }}
                  onClearAll={() => {
                    setRecentlyPlayed([]);
                    localStorage.removeItem('ais_recently_played');
                    setToast({ message: 'Listening history cleared' });
                  }}
                />
              </motion.div>
            ) : (
              <motion.div
                key="album"
                initial={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
                exit={{ opacity: 0, scale: 0.98, filter: 'blur(10px)' }}
                transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                className="h-full"
              >
                {activeCollection && (
                  <AlbumView 
                    collection={activeCollection} 
                    onPlaySong={handlePlaySong} 
                    nowPlaying={nowPlaying} 
                    isPlaying={isPlaying} 
                    likedSongs={likedSongs}
                    downloadedSongs={downloadedSongs}
                    onToggleLike={toggleLike}
                    onToggleDownload={toggleDownload}
                    onAddToQueue={handleAddToQueue}
                    onPlayNext={handlePlayNext}
                    onAddToPlaylist={setPlaylistModalSong}
                    onDontRecommend={handleDontRecommend}
                    onSongContextMenu={handleOpenSongContextMenu}
                    onRemoveFromPlaylist={
                      activeCollection && playlists.some(p => p.id === activeCollection.id) 
                        ? (song) => {
                            removeSongFromPlaylist(activeCollection.id, song.id);
                            setActiveCollection(prev => prev ? { ...prev, songs: prev.songs.filter(s => s.id !== song.id) } : null);
                          }
                        : undefined
                    }
                    onShare={handleShare}
                    playlists={playlists}
                    onDeletePlaylist={(id) => { deletePlaylist(id); setActiveCollection(null); }}
                    onMergePlaylist={(targetId, sourceId) => { mergePlaylists(targetId, sourceId); setActiveCollection(null); }}                  
                    />
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>

      <AnimatePresence>
        {showRightSidebar && (
          <>
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="md:hidden fixed inset-0 z-40 bg-black/20 backdrop-blur-sm"
              onClick={() => setShowRightSidebar(false)}
            />
            <RightSidebar currentTime={currentPlaybackTime} nowPlaying={nowPlaying} queue={queue} onReorder={handleReorderQueue} onSongContextMenu={handleOpenSongContextMenu} />
          </>
        )}
      </AnimatePresence>


      {showCreatePlaylistModal && (
        <div className="fixed inset-0 z-[100] bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-sm">
            <h3 className="text-lg font-bold mb-4">Create Playlist</h3>
            <div className="flex gap-2 mb-2">
              <input 
                type="text" 
                value={newPlaylistName}
                onChange={e => setNewPlaylistName(e.target.value)}
                placeholder="Playlist Name" 
                className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#fe5f64]"
              />
              <button 
                onClick={() => {
                  if(newPlaylistName.trim()) {
                    const p = createPlaylist(newPlaylistName.trim());
                    setNewPlaylistName('');
                    setShowCreatePlaylistModal(false);
                    showToast(`Created ${p.title}`);
                  }
                }}
                className="px-4 py-2 bg-[#fe5f64] text-white font-bold rounded-lg hover:bg-[#A84A22] transition-colors"
              >
                Create
              </button>
            </div>
            <button 
              onClick={() => { setShowCreatePlaylistModal(false); setNewPlaylistName(''); }}
              className="w-full py-2 text-gray-500 font-medium mt-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
      {playlistModalSong && (
        <div className="fixed inset-0 z-[100] bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-sm">
            <h3 className="text-lg font-bold mb-4">Add to Playlist</h3>
            
            <div className="flex gap-2 mb-6">
              <input 
                type="text" 
                value={newPlaylistName}
                onChange={e => setNewPlaylistName(e.target.value)}
                placeholder="New Playlist Name" 
                className="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-[#fe5f64]"
              />
              <button 
                onClick={() => {
                  if(newPlaylistName.trim()) {
                    const p = createPlaylist(newPlaylistName.trim());
                    addSongToPlaylist(p.id, playlistModalSong);
                    setNewPlaylistName('');
                    setPlaylistModalSong(null);
                    showToast(`Added to ${p.title}`);
                  }
                }}
                className="bg-[#fe5f64] text-white px-4 py-2 rounded-lg text-sm font-bold"
              >
                Create
              </button>
            </div>
            
            <div className="space-y-2 max-h-60 overflow-y-auto hide-scrollbar mb-4">
              {playlists.map(p => (
                <button 
                  key={p.id}
                  onClick={() => {
                    addSongToPlaylist(p.id, playlistModalSong);
                    setPlaylistModalSong(null);
                    showToast(`Added to ${p.title}`);
                  }}
                  className="w-full flex items-center gap-3 p-2 hover:bg-gray-100 rounded-lg transition-colors text-left"
                >
                  <img src={p.coverUrl} className="w-10 h-10 rounded object-cover" />
                  <span className="font-semibold text-sm truncate">{p.title}</span>
                </button>
              ))}
              {playlists.length === 0 && <p className="text-sm text-gray-500 text-center py-4">No playlists yet</p>}
            </div>
            
            <button 
              onClick={() => { setPlaylistModalSong(null); setNewPlaylistName(''); }}
              className="w-full py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-lg text-sm font-bold transition-colors"
            >
              Cancel
            </button>
          </div>
        </div>
      )}
      <Player 
          song={nowPlaying} 
          isPlaying={isPlaying} 
          onTogglePlay={() => setIsPlaying(!isPlaying)} 
          onToggleRightSidebar={() => setShowRightSidebar(!showRightSidebar)}
          onNext={handleNext}
          onPrev={handlePrev}
          onSongContextMenu={handleOpenSongContextMenu}
          isShuffle={isShuffle}
          repeatMode={repeatMode}
          onToggleShuffle={() => setIsShuffle(!isShuffle)}
          onToggleRepeat={() => {
            if (repeatMode === 'none') setRepeatMode('all');
            else if (repeatMode === 'all') setRepeatMode('one');
            else setRepeatMode('none');
          }}
          isLiked={nowPlaying ? likedSongs.some(s => s.id === nowPlaying.id) : false}
          onToggleLike={() => nowPlaying && toggleLike(nowPlaying)}
          onShare={handleShare}
          currentTime={currentPlaybackTime}
          duration={duration}
          isBuffering={isBuffering}
          isMini={isScrolled}
          volume={volume * crossfadeVolume}
          onVolumeChange={setVolume}
          playbackRate={playbackRate}
          onPlaybackRateChange={setPlaybackRate}
          onFadeOut={handleFadeOut}
          onSeek={(time) => {
            if (playerRef.current) {
               playerRef.current.seekTo(time, 'seconds');
            }
            setCurrentPlaybackTime(time);
          }}
        />
        <div className="absolute opacity-[0.01] pointer-events-none -z-10 w-[200px] h-[200px] overflow-hidden">
          <ReactPlayer
            ref={playerRef}
            url={nowPlayingUrl || ""}
            playing={isPlaying}
            volume={volume * crossfadeVolume}
            config={{ youtube: { playerVars: { playsinline: 1, autoplay: 1 } }, file: { forceAudio: true, attributes: { crossOrigin: 'anonymous' } } }}
            onReady={() => {
              try {
                 const internal = playerRef.current?.getInternalPlayer();
                 if (internal && internal instanceof HTMLMediaElement) {
                    if (!audioCtxRef.current) {
                        const Ctx = window.AudioContext || (window as any).webkitAudioContext;
                        audioCtxRef.current = new Ctx();
                        
                        sourceNodeRef.current = audioCtxRef.current.createMediaElementSource(internal);
                        
                        // Dynamic gain/normalization
                        compressorNodeRef.current = audioCtxRef.current.createDynamicsCompressor();
                        compressorNodeRef.current.threshold.value = -24;
                        compressorNodeRef.current.knee.value = 30;
                        compressorNodeRef.current.ratio.value = 12;
                        compressorNodeRef.current.attack.value = 0.003;
                        compressorNodeRef.current.release.value = 0.25;

                        // Visualizer analyzer
                        analyzerNodeRef.current = audioCtxRef.current.createAnalyser();
                        analyzerNodeRef.current.fftSize = 256;
                        setAnalyzerNode(analyzerNodeRef.current);
                        
                        gainNodeRef.current = audioCtxRef.current.createGain();
                        gainNodeRef.current.gain.value = volume;
                        
                        sourceNodeRef.current.connect(compressorNodeRef.current);
                        compressorNodeRef.current.connect(gainNodeRef.current);
                        gainNodeRef.current.connect(analyzerNodeRef.current);
                        analyzerNodeRef.current.connect(audioCtxRef.current.destination);
                    }
                    if (audioCtxRef.current.state === 'suspended') {
                        audioCtxRef.current.resume();
                    }
                 }
              } catch (err) {
                 console.error("Web Audio API Error", err);
              }
            }}
            onPlay={() => {
              if (audioCtxRef.current?.state === 'suspended') {
                 audioCtxRef.current.resume();
              }
            }}
            playbackRate={playbackRate}
            width="200px" 
            height="200px"
            controls={false}
            progressInterval={50}
            onProgress={handleProgress}
            onDuration={(d) => setDuration(d)}
            onBuffer={() => setIsBuffering(true)}
            onBufferEnd={() => setIsBuffering(false)}
            onError={handleTrackPlaybackError}
            onEnded={() => {
               if (repeatMode === 'one') {
                  if (playerRef.current) {
                    playerRef.current.seekTo(0);
                  }
               } else {
                  handleNext();
               }
            }}
          />
        </div>


      <AnimatePresence>
        {showShortcuts && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] bg-black/40 backdrop-blur-sm flex items-center justify-center p-4"
            onClick={() => setShowShortcuts(false)}
          >
            <motion.div 
              initial={{ scale: 0.95 }} animate={{ scale: 1 }} exit={{ scale: 0.95 }}
              onClick={e => e.stopPropagation()}
              className="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-md"
            >
              <h3 className="text-xl font-bold mb-6">Keyboard Shortcuts</h3>
              <div className="space-y-4">
                <ShortcutRow keys={['Space']} label="Play / Pause" />
                <ShortcutRow keys={['N']} label="Next Track" />
                <ShortcutRow keys={['P']} label="Previous Track" />
                <ShortcutRow keys={['→']} label="Seek Forward 10s" />
                <ShortcutRow keys={['←']} label="Seek Backward 10s" />
                <ShortcutRow keys={['↑']} label="Volume Up" />
                <ShortcutRow keys={['↓']} label="Volume Down" />
                <ShortcutRow keys={['?']} label="Toggle Shortcuts" />
              </div>
              <button 
                onClick={() => setShowShortcuts(false)}
                className="w-full mt-8 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 font-bold rounded-lg transition-colors"
              >
                Close
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <SongContextMenu 
        isOpen={!!songContextMenu}
        position={{ x: songContextMenu?.x || 0, y: songContextMenu?.y || 0 }}
        song={songContextMenu?.song || null}
        onClose={() => setSongContextMenu(null)}
        onDontRecommend={handleDontRecommend}
        onPlaySong={(song) => handlePlaySong(song)}
        onPlayNext={handlePlayNext}
        onAddToQueue={handleAddToQueue}
        onAddToPlaylist={(song) => setPlaylistModalSong(song)}
        onRemoveFromPlaylist={songContextMenu?.onRemoveFromPlaylist}
        onToggleLike={toggleLike}
        isLiked={songContextMenu?.song ? likedSongs.some(s => s.id === songContextMenu.song.id) : false}
        onToggleDownload={toggleDownload}
        isDownloaded={songContextMenu?.song ? downloadedSongs.some(s => s.id === songContextMenu.song.id) : false}
        onShare={(song) => handleShare({ type: 'song', id: song.id, name: song.title })}
      />
    </div>
  );
}

function ShortcutRow({ keys, label }: { keys: string[], label: string }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-sm font-semibold text-gray-600">{label}</span>
      <div className="flex gap-1.5">
        {keys.map(k => (
          <kbd key={k} className="px-2 py-1 bg-gray-100 border border-gray-200 rounded text-xs font-mono font-bold text-gray-800 min-w-[24px] text-center">
            {k}
          </kbd>
        ))}
      </div>
    </div>
  );
}
