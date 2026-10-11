import { SONGS } from '../data';
import { useContent } from '../hooks/useContent';
import { Collection, Song } from '../types';
import { motion, AnimatePresence } from 'motion/react';
import { Play, Download, MoreVertical, Merge, Trash2, History as HistoryIcon, Music2, Compass } from 'lucide-react';
import React, { useState, useEffect, useMemo } from 'react';
import { usePWAInstall } from '../hooks/usePWAInstall';
import { SongImage } from './SongImage';

const FALLBACK_IMG = 'https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?w=400&q=80';

// Helper function to evaluate genre similarity across subgenres, related styles and cultures
function getGenreSimilarity(songGenre?: string, targetGenre?: string): number {
  if (!songGenre || !targetGenre) return 0;
  const s = songGenre.toLowerCase().trim();
  const t = targetGenre.toLowerCase().trim();

  if (s === t) return 1.0;
  if (s.includes(t) || t.includes(s)) return 0.85;

  // Cultural and stylistic affinity clusters
  const clusters = [
    ['indian love', 'indian', 'bollywood', 'hindi', 'punjabi', 'sad', 'romantic'],
    ['pop', 'dance', 'synth-pop', 'alternative pop', 'j-pop', 'k-pop', 'dance-pop'],
    ['hip-hop', 'rap', 'hip-hop/rap', 'trap', 'r&b', 'soul'],
    ['rock', 'alternative', 'indie rock', 'hard rock', 'pop rock'],
    ['k-pop', 'j-pop', 'asian pop'],
    ['acoustic', 'folk', 'singer/songwriter', 'indie']
  ];

  for (const cluster of clusters) {
    const hasS = cluster.some(k => s.includes(k) || k.includes(s));
    const hasT = cluster.some(k => t.includes(k) || k.includes(t));
    if (hasS && hasT) return 0.75;
  }

  return 0;
}

export function HomeView({ 
  onCollectionClick, 
  playlists = [],
  onPlaySong,
  onGenreClick,
  downloadedSongs,
  onDeletePlaylist, 
  onMergePlaylist,
  recentlyPlayedHistory = [],
  likedSongs = [],
  notRecommendedSongIds = [],
  onSongContextMenu
}: { 
  onCollectionClick: (c: Collection) => void;
  playlists?: Collection[];
  onPlaySong?: (song: Song, context: { songs: Song[] }) => void;
  downloadedSongs?: Song[];
  onGenreClick?: (genre: string) => void;
  onDeletePlaylist?: (id: string) => void;
  onMergePlaylist?: (targetId: string, sourceId: string) => void;
  recentlyPlayedHistory?: Song[];
  likedSongs?: Song[];
  notRecommendedSongIds?: string[];
  onSongContextMenu?: (e: React.MouseEvent, song: Song) => void;
}) {
  const { deferredPrompt, installPWA } = usePWAInstall();

  const [contextMenu, setContextMenu] = useState<{ x: number; y: number; playlistId: string } | null>(null);
  const [mergeMenu, setMergeMenu] = useState<{ x: number; y: number; sourcePlaylistId: string } | null>(null);

  useEffect(() => {
    const handleClick = () => {
      setContextMenu(null);
      setMergeMenu(null);
    };
    document.addEventListener('click', handleClick);
    return () => document.removeEventListener('click', handleClick);
  }, []);

  const handleContextMenu = (e: React.MouseEvent, playlistId: string) => {
    e.preventDefault();
    setContextMenu({ x: e.clientX, y: e.clientY, playlistId });
    setMergeMenu(null);
  };

  const { mixes, albums, songs: fetchedSongs, isLoading } = useContent();

  // Combine fetched catalog with SONGS to ensure complete coverage, excluding not recommended tracks
  const allCatalog = useMemo(() => {
    const combined = [...SONGS, ...fetchedSongs.filter(fs => !SONGS.some(ls => ls.id === fs.id))];
    const blockedSet = new Set(notRecommendedSongIds);
    return combined.filter(song => !blockedSet.has(song.id));
  }, [fetchedSongs, notRecommendedSongIds]);

  // Combine user signals: recently played tracks and explicitly liked tracks
  const userSignals = useMemo(() => {
    return [...(recentlyPlayedHistory || []), ...(likedSongs || [])];
  }, [recentlyPlayedHistory, likedSongs]);

  const hasEnoughHistory = userSignals.length > 0;

  // Track user choices & execute the recommendation algorithm
  const { recommendations, subtitleInfo, topGenreName } = useMemo(() => {
    if (!hasEnoughHistory || allCatalog.length === 0) {
      return { recommendations: [], subtitleInfo: '', topGenreName: '' };
    }

    const genreScores: Record<string, number> = {};
    const artistScores: Record<string, number> = {};
    const playedSongIds = new Set((recentlyPlayedHistory || []).map(s => s.id));
    const likedSongIds = new Set((likedSongs || []).map(s => s.id));

    // 1. Track user choices from recent history with recency decay
    (recentlyPlayedHistory || []).forEach((song, idx) => {
      // Recent plays are weighted higher (e.g. 5.0 for latest, down to 1.5)
      const recencyWeight = Math.max(1.5, 5.0 - idx * 0.35);
      if (song.genre) {
        const g = song.genre.trim();
        genreScores[g] = (genreScores[g] || 0) + recencyWeight;
      }
      if (song.artist) {
        const a = song.artist.trim();
        artistScores[a] = (artistScores[a] || 0) + recencyWeight;
      }
    });

    // 2. Track user choices from liked songs (+4.0 strong explicit endorsement)
    (likedSongs || []).forEach(song => {
      if (song.genre) {
        const g = song.genre.trim();
        genreScores[g] = (genreScores[g] || 0) + 4.0;
      }
      if (song.artist) {
        const a = song.artist.trim();
        artistScores[a] = (artistScores[a] || 0) + 4.0;
      }
    });

    const sortedGenres = Object.entries(genreScores).sort((a, b) => b[1] - a[1]);
    const sortedArtists = Object.entries(artistScores).sort((a, b) => b[1] - a[1]);

    const topGenres = sortedGenres.map(e => e[0]);
    const topArtists = sortedArtists.map(e => e[0]);

    // Descriptive reason explaining what choices the algorithm is tracking
    let subtitle = '';
    if (topGenres.length > 0 && topArtists.length > 0) {
      subtitle = `Curated based on your love for ${topGenres[0]} & ${topArtists[0]}`;
    } else if (topGenres.length > 0) {
      subtitle = `Curated based on your affinity for ${topGenres[0]}`;
    } else if (topArtists.length > 0) {
      subtitle = `Curated based on your plays from ${topArtists[0]}`;
    } else {
      subtitle = 'Recommended for you based on your recent listening choices';
    }

    interface ScoredSong {
      song: Song;
      score: number;
      isHeard: boolean;
      genreMatch: boolean;
      artistMatch: boolean;
    }

    const scoredList: ScoredSong[] = [];
    const seenSongIds = new Set<string>();

    allCatalog.forEach(song => {
      if (seenSongIds.has(song.id)) return;
      seenSongIds.add(song.id);

      const isHeard = playedSongIds.has(song.id);
      let genreScore = 0;
      let artistScore = 0;
      let hasGenreMatch = false;
      let hasArtistMatch = false;

      // Check genre affinity
      if (song.genre) {
        for (const [userGenre, weight] of sortedGenres) {
          const sim = getGenreSimilarity(song.genre, userGenre);
          if (sim > 0) {
            genreScore = Math.max(genreScore, sim * weight * 12);
            hasGenreMatch = true;
          }
        }
      }

      // Check artist affinity
      if (song.artist) {
        for (const [userArtist, weight] of sortedArtists) {
          const sArtist = song.artist.toLowerCase();
          const uArtist = userArtist.toLowerCase();
          if (sArtist.includes(uArtist) || uArtist.includes(sArtist)) {
            artistScore = Math.max(artistScore, weight * 16);
            hasArtistMatch = true;
          }
        }
      }

      // Filter: only songs that genuinely match user's tracked choices!
      if (!hasGenreMatch && !hasArtistMatch) {
        return;
      }

      let totalScore = genreScore + artistScore;

      // UNHEARD DISCOVERY BOOST:
      // Prioritize tracks the user hasn't heard yet!
      // Gives a high discovery bonus (+30) so unheard songs in matching genres rank FIRST!
      if (!isHeard) {
        totalScore += 30;
      }

      // Small bonus if already liked
      if (likedSongIds.has(song.id)) {
        totalScore += 5;
      }

      scoredList.push({
        song,
        score: totalScore,
        isHeard,
        genreMatch: hasGenreMatch,
        artistMatch: hasArtistMatch
      });
    });

    // Sort: Unheard tracks first, then highest score descending!
    scoredList.sort((a, b) => {
      if (a.isHeard !== b.isHeard) {
        return a.isHeard ? 1 : -1; // Unheard tracks always prioritized
      }
      return b.score - a.score;
    });

    let result = scoredList.map(s => s.song);

    // If catalog has fewer than 5 matching candidates, pad with other unheard catalog tracks
    if (result.length < 5) {
      const moreUnheard = allCatalog.filter(s => 
        !playedSongIds.has(s.id) && 
        !result.some(r => r.id === s.id)
      );
      result = [...result, ...moreUnheard.slice(0, 5 - result.length)];
    }

    return {
      recommendations: result.slice(0, 15),
      subtitleInfo: subtitle,
      topGenreName: topGenres[0] || ''
    };
  }, [allCatalog, userSignals, recentlyPlayedHistory, likedSongs, hasEnoughHistory]);

  // Global Trending Tracks (used as the primary hero section initially, or secondary when history exists)
  const trendingSongs = useMemo(() => {
    return allCatalog.slice(0, 15);
  }, [allCatalog]);

  const popularGenres = ['Indian Love', 'Pop', 'Hip-Hop', 'R&B', 'K-Pop', 'Rock', 'Acoustic', 'Sad'];

  return (
    <>
      <div className="px-4 md:px-8 pb-32 pt-6">

        {/* 
          CASE 1: USER HAS NOT LISTENED TO SONGS YET (OR JUST ARRIVED)
          Show TRENDING NOW prominently as the #1 hero section!
        */}
        {!hasEnoughHistory && (
          <motion.section 
            className="mb-12"
            initial="hidden"
            animate="show"
            variants={{
              hidden: { opacity: 0, y: 10 },
              show: { opacity: 1, y: 0, transition: { staggerChildren: 0.05 } }
            }}
          >
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-[24px] font-bold text-gray-900 tracking-tight">Trending Now</h2>
                <p className="text-sm text-gray-500 mt-0.5">Top trending songs streaming globally right now • Tap any track to play</p>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
              {trendingSongs.slice(0, 10).map((song) => (
                <motion.div 
                  key={song.id}
                  variants={{
                    hidden: { opacity: 0, y: 15, scale: 0.95 },
                    show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
                  }}
                  whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
                  className="cursor-pointer group relative"
                  onClick={() => onPlaySong?.(song, { songs: trendingSongs })}
                  onContextMenu={(e) => onSongContextMenu?.(e, song)}
                  data-song-id={song.id}
                >
                  <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] relative bg-gray-100">
                    <SongImage 
                      song={song}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                      alt={song.title} 
                    />
                    <div className="absolute inset-0 bg-black/25 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                      <div className="w-11 h-11 rounded-full bg-white text-gray-900 flex items-center justify-center pl-1 shadow-lg transform group-hover:scale-105 transition-transform">
                        <Play size={20} fill="currentColor" />
                      </div>
                    </div>
                    {song.genre && (
                      <div className="absolute top-2 left-2 bg-black/50 backdrop-blur-md text-white text-[10px] font-medium px-2 py-0.5 rounded-full">
                        {song.genre}
                      </div>
                    )}
                  </div>
                  <h3 className="font-semibold text-gray-900 truncate leading-tight tracking-tight text-sm md:text-base">{song.title}</h3>
                  <p className="text-[13px] font-medium text-gray-500 truncate mt-0.5">{song.artist}</p>
                </motion.div>
              ))}
            </div>
          </motion.section>
        )}

        {/* 
          CASE 2: USER HAS LISTENED TO SONGS (TRACKING USER CHOICES)
          Show RECOMMENDED FOR YOU prominently as the #1 hero section!
        */}
        {hasEnoughHistory && recommendations.length > 0 && (
          <motion.section 
            className="mb-12"
            initial="hidden"
            animate="show"
            variants={{
              hidden: { opacity: 0, y: 10 },
              show: { opacity: 1, y: 0, transition: { staggerChildren: 0.05 } }
            }}
          >
            <div className="flex items-center justify-between mb-4">
              <div>
                {topGenreName && (
                  <div className="flex items-center gap-2 mb-1">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">
                      Genre: {topGenreName}
                    </span>
                  </div>
                )}
                <h2 className="text-[24px] font-bold text-gray-900 tracking-tight">Recommended for You</h2>
                <p className="text-sm text-gray-500 mt-0.5">{subtitleInfo}</p>
              </div>
            </div>

            {/* Horizontal snap carousel of recommended tracks */}
            <div className="flex overflow-x-auto gap-4 md:gap-6 pb-4 snap-x [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
              {recommendations.map((song) => {
                return (
                  <motion.div 
                    key={song.id}
                    variants={{
                      hidden: { opacity: 0, y: 15, scale: 0.95 },
                      show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
                    }}
                    whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
                    className="cursor-pointer group relative min-w-[150px] md:min-w-[185px] w-[150px] md:w-[185px] snap-start shrink-0"
                    onClick={() => onPlaySong?.(song, { songs: recommendations })}
                    onContextMenu={(e) => onSongContextMenu?.(e, song)}
                    data-song-id={song.id}
                  >
                    <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] relative bg-gray-100">
                      <SongImage 
                        song={song}
                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                        alt={song.title} 
                      />
                      <div className="absolute inset-0 bg-black/25 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        <div className="w-11 h-11 rounded-full bg-white text-gray-900 flex items-center justify-center pl-1 shadow-lg transform group-hover:scale-105 transition-transform">
                          <Play size={20} fill="currentColor" />
                        </div>
                      </div>
                      
                      {/* Song Genre badge */}
                      {song.genre && (
                        <div className="absolute top-2 left-2 bg-black/50 backdrop-blur-md text-white text-[10px] font-medium px-2 py-0.5 rounded-full">
                          {song.genre}
                        </div>
                      )}
                    </div>
                    <h3 className="font-semibold text-gray-900 truncate leading-tight tracking-tight text-sm md:text-base">{song.title}</h3>
                    <p className="text-[13px] font-medium text-gray-500 truncate mt-0.5">{song.artist}</p>
                  </motion.div>
                );
              })}
            </div>
          </motion.section>
        )}

        {/* 
          WHEN USER HAS HISTORY, TRENDING NOW IS RENDERED BELOW RECOMMENDATIONS 
          SO GLOBAL MUSIC IS ALWAYS ACCESSIBLE
        */}
        {hasEnoughHistory && (
          <motion.section 
            className="mb-12"
            initial="hidden"
            animate="show"
            variants={{
              hidden: { opacity: 0 },
              show: { opacity: 1, transition: { staggerChildren: 0.05 } }
            }}
          >
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-[22px] font-bold text-gray-900 tracking-tight">Trending Now</h2>
                <p className="text-sm text-gray-500 mt-0.5">Global chart toppers and popular hits</p>
              </div>
            </div>

            <div className="flex overflow-x-auto gap-4 md:gap-6 pb-4 snap-x [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
              {trendingSongs.slice(0, 10).map((song) => (
                <motion.div 
                  key={song.id}
                  variants={{
                    hidden: { opacity: 0, y: 15, scale: 0.95 },
                    show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
                  }}
                  whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
                  className="cursor-pointer group relative min-w-[140px] md:min-w-[170px] w-[140px] md:w-[170px] snap-start shrink-0"
                  onClick={() => onPlaySong?.(song, { songs: trendingSongs })}
                  onContextMenu={(e) => onSongContextMenu?.(e, song)}
                  data-song-id={song.id}
                >
                  <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] relative bg-gray-100">
                    <SongImage 
                      song={song}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" 
                      alt={song.title} 
                    />
                    <div className="absolute inset-0 bg-black/25 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                      <div className="w-10 h-10 rounded-full bg-white text-gray-900 flex items-center justify-center pl-1 shadow-lg">
                        <Play size={18} fill="currentColor" />
                      </div>
                    </div>
                  </div>
                  <h3 className="font-semibold text-gray-900 truncate leading-tight tracking-tight text-sm">{song.title}</h3>
                  <p className="text-[12px] font-medium text-gray-500 truncate mt-0.5">{song.artist}</p>
                </motion.div>
              ))}
            </div>
          </motion.section>
        )}

        {/* EXPLORE BY GENRE PILLS */}
        <section className="mb-12">
          <div className="flex items-center gap-2 mb-4">
            <Compass size={18} className="text-[#fe5f64]" />
            <h2 className="text-[20px] font-bold text-gray-900 tracking-tight">Explore Genres</h2>
          </div>
          <div className="flex flex-wrap gap-2.5">
            {popularGenres.map((genre) => (
              <button
                key={genre}
                onClick={() => onGenreClick?.(genre)}
                className="px-4 py-2 rounded-xl text-sm font-semibold bg-white border border-gray-200/80 hover:border-[#fe5f64] hover:text-[#fe5f64] shadow-sm hover:shadow transition-all active:scale-95"
              >
                {genre}
              </button>
            ))}
          </div>
        </section>

        {/* USER PLAYLISTS */}
        {playlists.length > 0 && (
          <motion.section 
            className="mb-12"
            initial="hidden"
            animate="show"
            variants={{
              hidden: { opacity: 0 },
              show: { opacity: 1, transition: { staggerChildren: 0.08, delayChildren: 0.1 } }
            }}
          >
            <h2 className="text-[22px] font-bold text-gray-900 mb-5 tracking-tight">Your Playlists</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
              {playlists.map((playlist) => (
                <motion.div 
                  key={playlist.id}
                  variants={{
                    hidden: { opacity: 0, y: 15, scale: 0.95 },
                    show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
                  }}
                  whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
                  className="cursor-pointer group relative"
                  onClick={() => onCollectionClick(playlist)}
                  onContextMenu={(e) => handleContextMenu(e, playlist.id)}
                  onDoubleClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    handleContextMenu(e, playlist.id);
                  }}
                >
                  <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_8px_20px_rgb(0,0,0,0.12)] bg-gray-100 flex items-center justify-center relative">
                    {playlist.songs.length > 0 ? (
                       <SongImage song={playlist.songs[0]} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700 ease-out" alt={playlist.title} />
                    ) : (
                       <div className="w-full h-full bg-gradient-to-br from-gray-200 to-gray-300" />
                    )}
                    <div className="absolute bottom-2 right-2 bg-black/60 backdrop-blur-sm text-white text-[10px] font-bold px-2 py-1 rounded-md">
                       {playlist.songs.length}
                    </div>
                  </div>
                  <h3 className="font-semibold text-gray-900 truncate leading-tight tracking-tight">{playlist.title}</h3>
                  <p className="text-[13px] font-medium text-gray-500 truncate mt-0.5">Playlist</p>
                </motion.div>
              ))}
            </div>
          </motion.section>
        )}

        {/* PWA INSTALL PROMPT */}
        <AnimatePresence>
          {deferredPrompt && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              className="fixed bottom-[140px] left-4 right-4 md:left-auto md:right-8 md:w-96 bg-[#212121] text-white p-4 rounded-2xl shadow-2xl flex flex-col gap-3 z-40 border border-white/10"
            >
              <div className="flex gap-4 items-center">
                <div className="w-12 h-12 bg-gradient-to-br from-[#fe5f64] to-[#E58158] rounded-xl flex items-center justify-center shadow-lg">
                  <Download size={24} className="text-white" />
                </div>
                <div className="flex-1">
                  <h4 className="font-bold text-sm leading-tight text-white/90">Install App</h4>
                  <p className="text-xs text-white/60 leading-tight mt-1">Get a faster, native-like experience on your home screen.</p>
                </div>
              </div>
              <button 
                onClick={installPWA}
                className="w-full bg-[#fe5f64] hover:bg-[#b04a20] text-white text-sm font-bold py-2.5 rounded-xl transition-colors active:scale-[0.98]"
              >
                Add to Home Screen
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* CONTEXT MENU FOR PLAYLISTS */}
      {contextMenu && (
        <div 
          className="fixed z-[100] w-48 bg-white rounded-lg shadow-xl border border-gray-100 py-1"
          style={{ top: contextMenu.y, left: contextMenu.x }}
          onClick={(e) => e.stopPropagation()}
        >
          {playlists && playlists.length > 1 && (
            <button 
              className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2"
              onClick={() => {
                setMergeMenu({ x: contextMenu.x + 10, y: contextMenu.y + 10, sourcePlaylistId: contextMenu.playlistId });
                setContextMenu(null);
              }}
            >
              <Merge size={16} /> Merge Playlist...
            </button>
          )}
          <button 
            className="w-full text-left px-4 py-2 text-sm flex items-center gap-2 hover:bg-gray-50 text-[#fe5f64]"
            onClick={() => {
              onDeletePlaylist?.(contextMenu.playlistId);
              setContextMenu(null);
            }}
          >
            <Trash2 size={16} /> Delete Playlist
          </button>
        </div>
      )}

      {/* MERGE PLAYLIST MENU */}
      {mergeMenu && (
        <div 
          className="fixed z-[100] w-56 bg-white rounded-lg shadow-xl border border-gray-100 py-1"
          style={{ top: mergeMenu.y, left: mergeMenu.x }}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase">Merge with...</div>
          {playlists?.filter(p => p.id !== mergeMenu.sourcePlaylistId).map(p => (
            <button 
              key={p.id}
              className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 truncate"
              onClick={() => {
                onMergePlaylist?.(p.id, mergeMenu.sourcePlaylistId);
                setMergeMenu(null);
              }}
            >
              {p.title}
            </button>
          ))}
        </div>
      )}
    </>
  );
}