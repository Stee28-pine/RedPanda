import React, { useState, useEffect } from 'react';
import { motion } from 'motion/react';
import { Play, ChevronLeft, Mic2, Pause, Clock, BookmarkPlus, Bookmark as BookmarkIcon, Trash2 } from 'lucide-react';
import { Bookmark } from '../types';
import { Song } from '../types';

const PODCAST_SHOWS = [
  { name: "The Joe Rogan Experience", category: "Comedy", channel: "PowerfulJRE", image: "https://images.unsplash.com/photo-1581368135153-a506cf13b1e1?w=400&q=80" },
  { name: "WTF is…? (NIKHIL KAMATH)", category: "Business", channel: "Nikhil Kamath", image: "https://images.unsplash.com/photo-1593642632823-8f785ba67e45?w=400&q=80" },
  { name: "RAJ SHAMANI", category: "Business", channel: "Raj Shamani", image: "https://images.unsplash.com/photo-1556761175-5973dc0f32b7?w=400&q=80" },
  { name: "LEX FRIDMAN", category: "Technology", channel: "Lex Fridman", image: "https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&q=80" },
  { name: "The Daily", category: "Storytelling", channel: "The New York Times", image: "https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&q=80" },
  { name: "Crime Junkie", category: "Storytelling", channel: "Crime Junkie", image: "https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?w=400&q=80" },
  { name: "The Mel Robbins Podcast", category: "Storytelling", channel: "Mel Robbins", image: "https://images.unsplash.com/photo-1552664730-d307ca884978?w=400&q=80" },
  { name: "Call Her Daddy", category: "Comedy", channel: "Call Her Daddy", image: "https://images.unsplash.com/photo-1512418490979-92798cec1380?w=400&q=80" },
  { name: "Huberman Lab", category: "Technology", channel: "Andrew Huberman", image: "https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=400&q=80" },
  { name: "New Heights with Jason and Travis Kelce", category: "Comedy", channel: "New Heights", image: "https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?w=400&q=80" },
  { name: "Stuff You Should Know", category: "Storytelling", channel: "Stuff You Should Know", image: "https://images.unsplash.com/photo-1456324504439-367cee3b3c32?w=400&q=80" },
  { name: "SmartLess", category: "Comedy", channel: "SmartLess", image: "https://images.unsplash.com/photo-1527228113244-88f58b90ed06?w=400&q=80" },
  { name: "The Ranveer Show (TRS)", category: "Storytelling", channel: "BeerBiceps", image: "https://images.unsplash.com/photo-1516280440502-a27902d3eece?w=400&q=80" },
  { name: "Figuring Out", category: "Business", channel: "Raj Shamani", image: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=400&q=80" },
  { name: "The Desi Crime Podcast", category: "Storytelling", channel: "Desi Studios", image: "https://images.unsplash.com/photo-1509822929063-6b6cfc9b42f2?w=400&q=80" },
  { name: "Finshots Daily", category: "Business", channel: "Finshots", image: "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=400&q=80" },
  { name: "The Stories of Mahabharata", category: "Storytelling", channel: "Sudipta Bhawmik", image: "https://images.unsplash.com/photo-1588691522851-9e73b22415d8?w=400&q=80" },
  { name: "Paisa Vaisa", category: "Business", channel: "IVM Podcasts", image: "https://images.unsplash.com/photo-1579621970588-a3f5ce599d6d?w=400&q=80" }
];

const CATEGORIES = ['All', 'Technology', 'Storytelling', 'Business', 'Comedy'];
const YEARS = ['All Time', '2024', '2023', '2022', '2021', '2020', '2019', '2018'];

export function PodcastsView({ searchQuery, onSearchChange, onPlaySong, nowPlaying, isPlaying, likedSongs, onToggleLike, currentTime, bookmarks, onAddBookmark, onRemoveBookmark, onSeekToTime }: {
  searchQuery?: string;
  onSearchChange?: (q: string) => void;
  onPlaySong: (song: Song) => void;
  nowPlaying: Song | null;
  isPlaying: boolean;
  likedSongs: Song[];
  onToggleLike: (song: Song) => void;
  currentTime?: number;
  bookmarks?: Bookmark[];
  onAddBookmark?: (songId: string, timestamp: number, note: string) => void;
  onRemoveBookmark?: (id: string) => void;
  onSeekToTime?: (time: number) => void;
}) {
  const [noteText, setNoteText] = useState('');
  
  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  const [activeCategory, setActiveCategory] = useState('All');
  const [selectedShow, setSelectedShow] = useState<string | null>(null);
  const [selectedYear, setSelectedYear] = useState('All Time');
  const [episodes, setEpisodes] = useState<Song[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Handle Global Search updates
  useEffect(() => {
    if (searchQuery && searchQuery.trim() !== '') {
      setSelectedShow(null);
      const timer = setTimeout(() => {
        fetchEpisodes(searchQuery + " podcast");
      }, 500);
      return () => clearTimeout(timer);
    } else if (!selectedShow) {
      setEpisodes([]);
    }
  }, [searchQuery]);

  // Handle Show Selection
  useEffect(() => {
    if (selectedShow) {
      const showData = PODCAST_SHOWS.find(s => s.name === selectedShow);
      const yearQuery = selectedYear === 'All Time' ? '' : ` ${selectedYear}`;
      fetchEpisodes(selectedShow + " podcast full episode" + yearQuery, showData?.channel, selectedShow);
      if (onSearchChange) onSearchChange('');
    }
  }, [selectedShow, selectedYear]);

  const fetchEpisodes = async (query: string, targetChannel?: string, showNameStr?: string) => {
    setIsLoading(true);
    try {
      const ytRes = await fetch(`/api/search-podcasts?q=${encodeURIComponent(query)}`);
      const ytData = await ytRes.json();
      if (ytData.results) {
        let finalResults = ytData.results;
        
        // Filter strictly by channel if requested
        if (targetChannel) {
          const channelLower = targetChannel.toLowerCase();
          finalResults = ytData.results.filter((podcast: any) => {
             const artistLower = podcast.artist.toLowerCase();
             const titleLower = podcast.title.toLowerCase();
             const showNameLower = targetChannel ? targetChannel.toLowerCase() : "";
             const rawShowName = showNameStr ? showNameStr.toLowerCase() : query.replace(" podcast full episode", "").toLowerCase();
             
             // Very strict filtering as requested by user.
             // We only want episodes from the exact author/channel OR where the video explicitly titles itself as the show.
             return artistLower.includes(channelLower) || channelLower.includes(artistLower) || titleLower.includes(rawShowName);
          });
        }
        
        setEpisodes(finalResults.map((r: any) => ({ ...r, genre: 'Podcast' })));
      }
    } catch(e) {
      console.error("Podcast search failed", e);
    } finally {
      setIsLoading(false);
    }
  };

  const filteredShows = activeCategory === 'All' 
    ? PODCAST_SHOWS 
    : PODCAST_SHOWS.filter(s => s.category === activeCategory);

  const isSearchActive = (searchQuery && searchQuery.trim() !== '') || selectedShow !== null;

  return (
    <div className="px-4 md:px-8 py-6 pb-32">
      {!isSearchActive ? (
        <>
          <h1 className="text-3xl font-black text-gray-900 mb-6 tracking-tight">Podcasts</h1>
          
          {/* Category Navigation Bar */}
          <div className="flex gap-2 mb-8 overflow-x-auto hide-scrollbar pb-2">
            {CATEGORIES.map(cat => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                className={`px-6 py-2 rounded-full text-sm font-bold whitespace-nowrap transition-all ${
                  activeCategory === cat 
                    ? 'bg-[#fe5f64] text-white shadow-md' 
                    : 'bg-white border border-gray-200 text-gray-700 hover:border-[#fe5f64] hover:text-[#fe5f64]'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>

          {/* Podcast Channels Grid */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-4 md:gap-6">
            {filteredShows.map((show, i) => (
              <motion.div 
                key={show.name}
                variants={{
                  hidden: { opacity: 0, y: 15 },
                  show: { opacity: 1, y: 0, transition: { delay: i * 0.05 } }
                }}
                initial="hidden"
                animate="show"
                whileHover={{ y: -8, scale: 1.05, transition: { duration: 0.25, ease: 'easeOut' } }}
                className="cursor-pointer group"
                onClick={() => { setSelectedShow(show.name); setSelectedYear('All Time'); }}
              >
                <div className="aspect-square rounded-2xl overflow-hidden mb-3 shadow-[0_4px_15px_rgb(0,0,0,0.08)] group-hover:shadow-[0_20px_40px_rgba(254,95,100,0.25)] transition-shadow duration-300 bg-gray-100 flex items-center justify-center relative">
                  <div className="absolute inset-0 bg-gradient-to-br from-gray-800 to-black z-0" />
                  <img 
                    src={show.image} 
                    className="w-full h-full object-cover absolute inset-0 opacity-40 group-hover:opacity-60 transition-opacity duration-500 blend-overlay" 
                    alt="" 
                  />
                  <div className="z-10 p-4 text-center">
                    <Mic2 size={32} className="mx-auto mb-2 text-white/50" />
                    <span className="text-white font-black text-lg leading-tight tracking-tight drop-shadow-md">
                      {show.name}
                    </span>
                  </div>
                </div>
                <h3 className="font-bold text-gray-900 line-clamp-2 leading-tight text-sm">{show.name}</h3>
                <p className="text-[11px] font-bold text-[#fe5f64] mt-1 uppercase tracking-wider">{show.category}</p>
              </motion.div>
            ))}
          </div>
        </>
      ) : (
        <>
          {/* Episodes List View */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
            <div className="flex items-center gap-4">
              <button
                 onClick={() => { 
                   setSelectedShow(null); 
                   if (onSearchChange) onSearchChange(''); 
                 }}
                 className="p-2.5 rounded-full bg-white shadow-sm border border-gray-200 text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <ChevronLeft size={20} strokeWidth={2.5} />
              </button>
              <div>
                <h1 className="text-2xl font-black text-gray-900 tracking-tight">
                  {selectedShow ? selectedShow : `Results for "${searchQuery}"`}
                </h1>
                <p className="text-sm font-medium text-gray-500 mt-1">Audio Player Session Active</p>
              </div>
            </div>
          </div>

          {selectedShow && (
             <div className="mb-8">
               <div className="flex gap-2 overflow-x-auto hide-scrollbar pb-2">
                 {YEARS.map(year => (
                   <button
                     key={year}
                     onClick={() => setSelectedYear(year)}
                     className={`px-5 py-2 rounded-full text-sm font-bold whitespace-nowrap transition-all ${
                       selectedYear === year 
                         ? 'bg-[#fe5f64] text-white shadow-md' 
                         : 'bg-white border border-gray-200 text-gray-700 hover:border-[#fe5f64] hover:text-[#fe5f64]'
                     }`}
                   >
                     {year}
                   </button>
                 ))}
               </div>
             </div>
          )}

          {isLoading ? (
            <div className="flex justify-center items-center py-20">
              <div className="w-10 h-10 border-4 border-gray-200 border-t-[#fe5f64] rounded-full animate-spin"></div>
            </div>
          ) : episodes.length > 0 ? (
            <div className="flex flex-col gap-3 max-w-4xl">
              {episodes.map((podcast) => {
                const isCurrent = nowPlaying?.id === podcast.id;
                return (
                  <div key={podcast.id} className="flex flex-col">
                  <div 
                    className={`flex items-center gap-4 p-3 rounded-2xl transition-all group cursor-pointer border ${
                      isCurrent 
                        ? 'bg-[#fe5f64]/5 border-[#fe5f64]/20' 
                        : 'bg-white border-transparent hover:border-gray-200 hover:shadow-sm'
                    }`}
                    onClick={() => onPlaySong(podcast)}
                  >
                    <div className="w-16 h-16 md:w-20 md:h-20 rounded-xl overflow-hidden relative flex-shrink-0 bg-gray-100 shadow-sm">
                      <img src={podcast.coverUrl} className="w-full h-full object-cover" alt="" />
                      <div className="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        {isCurrent && isPlaying ? (
                          <Pause fill="white" size={24} className="text-white" />
                        ) : (
                          <Play fill="white" size={24} className="text-white ml-1" />
                        )}
                      </div>
                      {isCurrent && isPlaying && (
                        <div className="absolute inset-0 bg-black/40 flex items-center justify-center group-hover:opacity-0 transition-opacity">
                           <div className="flex gap-1 items-end h-4">
                             <div className="w-1 bg-[#fe5f64] rounded-full animate-[musicBar_1s_ease-in-out_infinite]" />
                             <div className="w-1 bg-[#fe5f64] rounded-full animate-[musicBar_1s_ease-in-out_infinite_0.2s]" />
                             <div className="w-1 bg-[#fe5f64] rounded-full animate-[musicBar_1s_ease-in-out_infinite_0.4s]" />
                           </div>
                        </div>
                      )}
                    </div>
                    
                    <div className="flex-1 min-w-0 pr-4">
                      <h3 className={`font-bold text-sm md:text-base line-clamp-2 leading-tight ${isCurrent ? 'text-[#fe5f64]' : 'text-gray-900'}`}>
                        {podcast.title}
                      </h3>
                      <p className="text-xs md:text-sm font-medium text-gray-500 mt-1.5 truncate">
                        {podcast.artist}
                      </p>
                    </div>
                    
                    <div className="flex-shrink-0 flex items-center gap-2">
                      <div className="hidden md:flex items-center text-xs font-bold text-gray-400 bg-gray-100 px-3 py-1.5 rounded-lg">
                        <Clock size={12} className="mr-1.5" />
                        {podcast.duration}
                      </div>
                    </div>
                  </div>
                  
                  {isCurrent && (
                    <div className="pl-[5.5rem] pr-4 pb-4 animate-in fade-in slide-in-from-top-2 duration-300">
                      <div className="bg-gray-50 border border-gray-100 rounded-xl p-4">
                        <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
                          <BookmarkIcon size={14} /> Bookmarks & Notes
                        </h4>
                        
                        <div className="flex items-center gap-2 mb-4">
                          <div className="text-sm font-bold text-[#fe5f64] bg-[#fe5f64]/10 px-2 py-1.5 rounded-md min-w-[3.5rem] text-center">
                            {formatTime(currentTime || 0)}
                          </div>
                          <input 
                            type="text"
                            placeholder="Add a note at this timestamp..."
                            className="flex-1 bg-white border border-gray-200 rounded-lg px-3 py-1.5 text-sm outline-none focus:border-[#fe5f64] focus:ring-1 focus:ring-[#fe5f64] transition-all"
                            value={noteText}
                            onChange={(e) => setNoteText(e.target.value)}
                            onKeyDown={(e) => {
                              if (e.key === 'Enter' && noteText.trim()) {
                                onAddBookmark?.(podcast.id, currentTime || 0, noteText.trim());
                                setNoteText('');
                              }
                            }}
                          />
                          <button 
                            className="bg-[#fe5f64] text-white p-1.5 rounded-lg hover:bg-red-500 transition-colors disabled:opacity-50"
                            disabled={!noteText.trim()}
                            onClick={() => {
                              if (noteText.trim()) {
                                onAddBookmark?.(podcast.id, currentTime || 0, noteText.trim());
                                setNoteText('');
                              }
                            }}
                          >
                            <BookmarkPlus size={18} />
                          </button>
                        </div>

                        {bookmarks?.filter(b => b.songId === podcast.id).length > 0 && (
                          <div className="space-y-2 mt-4 max-h-[200px] overflow-y-auto pr-2 hide-scrollbar">
                            {bookmarks.filter(b => b.songId === podcast.id).sort((a, b) => a.timestamp - b.timestamp).map(bm => (
                              <div key={bm.id} className="group flex items-start gap-3 bg-white p-2.5 rounded-lg border border-gray-100 hover:border-gray-200 transition-colors">
                                <button 
                                  onClick={() => onSeekToTime?.(bm.timestamp)}
                                  className="text-xs font-bold text-[#fe5f64] bg-[#fe5f64]/10 hover:bg-[#fe5f64]/20 px-2 py-1 rounded transition-colors"
                                >
                                  {formatTime(bm.timestamp)}
                                </button>
                                <p className="text-sm text-gray-700 flex-1 leading-tight">{bm.note}</p>
                                <button 
                                  onClick={() => onRemoveBookmark?.(bm.id)}
                                  className="opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-[#fe5f64] hover:bg-[#fe5f64]/10 rounded transition-all"
                                >
                                  <Trash2 size={14} />
                                </button>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-20">
              <Mic2 size={48} className="mx-auto text-gray-300 mb-4" />
              <p className="text-gray-500 font-bold text-lg">No episodes found.</p>
              <p className="text-gray-400 font-medium text-sm mt-1">Try another category or search term.</p>
            </div>
          )}
        </>
      )}
    </div>
  );
}
