import { useState, useEffect } from 'react';
import { Song, Collection } from '../types';
import { SONGS as localSongs, MIXES as localMixes, ALBUMS as localAlbums, RECENTLY_PLAYED as localRecentlyPlayed } from '../data';

export function useContent() {
  const [mixes, setMixes] = useState<Collection[]>(localMixes);
  const [recentlyPlayed, setRecentlyPlayed] = useState<Song[]>(localSongs.slice(0, 10));
  const [albums, setAlbums] = useState<Collection[]>(localAlbums);
  const [songs, setSongs] = useState<Song[]>(localSongs);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function fetchAll() {
      try {
        const res = await fetch("https://itunes.apple.com/us/rss/topsongs/limit=100/json");
        const data = await res.json();
        
        const topSongs: Song[] = data.feed.entry.map((entry: any) => {
          const previewUrl = entry.link.find((l: any) => l.attributes.type === 'audio/x-m4a')?.attributes.href;
          const coverUrl = entry['im:image'][entry['im:image'].length - 1].label.replace(/170x170/g, '400x400').replace(/60x60/g, '400x400').replace(/55x55/g, '400x400');
          return {
            id: entry.id.attributes['im:id'],
            title: entry['im:name'].label,
            artist: entry['im:artist'].label,
            album: entry['im:collection']['im:name'].label,
            coverUrl: coverUrl,
            genre: entry.category.attributes.label,
            duration: '0:30',
            durationSeconds: 30,
            previewUrl: previewUrl,
          };
        });

        // Merge local catalog with fetched top songs (preserving all local genre tracks)
        const mergedSongs: Song[] = [
          ...localSongs,
          ...topSongs.filter((ts: Song) => !localSongs.some(ls => ls.id === ts.id || ls.title.toLowerCase() === ts.title.toLowerCase()))
        ];
        setSongs(mergedSongs);

        const popSongs = topSongs.filter(s => s.genre === 'Pop' || s.genre.includes('Pop'));
        const countrySongs = topSongs.filter(s => s.genre === 'Country');
        const hipHopSongs = topSongs.filter(s => s.genre === 'Hip-Hop/Rap' || s.genre.includes('Rap'));
        const rockSongs = topSongs.filter(s => s.genre === 'Rock' || s.genre.includes('Alternative'));

        const newMixes: Collection[] = [
          { id: 'm1', type: 'mix', title: 'Top Hits Mix', subtitle: 'Global Top 100', coverUrl: topSongs[0]?.coverUrl || localMixes[0].coverUrl, songs: topSongs.slice(0, 20) },
          { id: 'm2', type: 'mix', title: 'Pop Mix', subtitle: 'Trending Pop Hits', coverUrl: popSongs[0]?.coverUrl || topSongs[1]?.coverUrl || localMixes[1].coverUrl, songs: popSongs.length > 0 ? popSongs : topSongs.slice(10, 30) },
          { id: 'm3', type: 'mix', title: 'Country Mix', subtitle: 'Top Country Hits', coverUrl: countrySongs[0]?.coverUrl || topSongs[2]?.coverUrl || localMixes[2].coverUrl, songs: countrySongs.length > 0 ? countrySongs : topSongs.slice(20, 40) },
          { id: 'm4', type: 'mix', title: 'Hip-Hop Mix', subtitle: 'Top Rap Hits', coverUrl: hipHopSongs[0]?.coverUrl || topSongs[3]?.coverUrl || localMixes[3].coverUrl, songs: hipHopSongs.length > 0 ? hipHopSongs : topSongs.slice(30, 50) },
          { id: 'm5', type: 'mix', title: 'Rock Mix', subtitle: 'Top Rock Hits', coverUrl: rockSongs[0]?.coverUrl || topSongs[4]?.coverUrl || localMixes[4].coverUrl, songs: rockSongs.length > 0 ? rockSongs : topSongs.slice(40, 60) }
        ];
        setMixes(newMixes);

        const albumRes = await fetch("https://itunes.apple.com/us/rss/topalbums/limit=20/json");
        const albumData = await albumRes.json();

        const topAlbums: Collection[] = albumData.feed.entry.map((entry: any, i: number) => {
          const coverUrl = entry['im:image'][entry['im:image'].length - 1].label.replace(/170x170/g, '400x400').replace(/60x60/g, '400x400');
          // get songs for this album by artist from top songs
          const artist = entry['im:artist'].label;
          let albumSongs = topSongs.filter(s => s.artist === artist);
          if (albumSongs.length === 0) albumSongs = topSongs.slice(i, i + 10);
          
          return {
            id: entry.id.attributes['im:id'],
            type: 'album',
            title: entry['im:name'].label,
            subtitle: entry['im:artist'].label,
            coverUrl: coverUrl,
            genre: entry.category.attributes.label,
            songs: albumSongs
          }
        });

        setAlbums(topAlbums.slice(0, 10));
        setRecentlyPlayed(topSongs.slice(15, 25));

      } catch (err) {
        console.error("Failed to fetch iTunes data:", err);
      } finally {
        setIsLoading(false);
      }
    }
    
    fetchAll();
  }, []);

  return { mixes, recentlyPlayed, albums, songs, isLoading };
}
