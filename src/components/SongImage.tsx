import React, { useState, useEffect } from 'react';
import { Song } from '../types';
import { Music } from 'lucide-react';

// Verified high-resolution artwork dictionary for top songs
export const VERIFIED_ARTWORK_MAP: Record<string, string> = {
  // Punjabi Hits
  'softly---karan aujla': 'https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/d3/08/bc/d308bc6a-20e1-6532-d933-35d1b429210e/5054197755538.jpg/600x600bb.jpg',
  'winning speech---karan aujla': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/48/7c/36/487c3668-f7a4-4b1a-e09e-c74dae124dd9/5063483578089_cover.jpg/600x600bb.jpg',
  'tauba tauba---karan aujla': 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/79/d2/01/79d201d2-e54d-5604-81fb-313f30db7219/198588533581.jpg/600x600bb.jpg',
  '52 bars---karan aujla': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/fc/bc/64/fcbc6417-8a88-7b5e-4490-8f53e537ffb0/859770181552_cover.jpg/600x600bb.jpg',
  'white brown black---karan aujla': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/0d/32/4d/0d324d1b-e705-c27a-5ddd-24630402bb85/5021732607164.jpg/600x600bb.jpg',
  'admiring you---karan aujla': 'https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/d3/08/bc/d308bc6a-20e1-6532-d933-35d1b429210e/5054197755538.jpg/600x600bb.jpg',
  'mexico---karan aujla': 'https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/f8/a9/26/f8a926d7-aae8-46a2-739d-5d1795f2fdf5/8905285022148.jpg/600x600bb.jpg',
  'on top---karan aujla': 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/ca/87/d4/ca87d416-2021-0eb1-f36a-fe01998c738d/5059950896060_cover.jpg/600x600bb.jpg',
  'g.o.a.t.---diljit dosanjh': 'https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/d2/89/ac/d289ac98-749e-3822-6b6e-b06aa4815715/859740651597_cover.jpg/600x600bb.jpg',
  'born to shine---diljit dosanjh': 'https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/d2/89/ac/d289ac98-749e-3822-6b6e-b06aa4815715/859740651597_cover.jpg/600x600bb.jpg',
  'kinni kinni---diljit dosanjh': 'https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/94/80/be/9480bec1-6ca2-5bae-a7da-d0e7c45633ce/859779847831_cover.jpg/600x600bb.jpg',
  'lover---diljit dosanjh': 'https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/8a/89/e4/8a89e445-d2c6-f8ac-a828-27818b0c1afe/859749638209_cover.jpg/600x600bb.jpg',
  'hass hass---diljit dosanjh': 'https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/af/11/f9/af11f978-7b08-8025-eb57-25682c8d9acb/5054197842245.jpg/600x600bb.jpg',
  'naina---diljit dosanjh': 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/bc/0f/35/bc0f35fd-96ad-c00d-4b28-83fa7420fa06/8901854102303.jpg/600x600bb.jpg',
  'lemonade---diljit dosanjh': 'https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/1b/2b/c5/1b2bc5ce-f6c1-c6c2-69bc-d5bc804701c7/859763661467_cover.jpg/600x600bb.jpg',
  'brown munde---ap dhillon': 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/26/a3/ac/26a3ac64-69e4-95ec-80ab-1f5a477537d2/859742042973_cover.jpg/600x600bb.jpg',
  'excuses---ap dhillon': 'https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/47/47/ac/4747ac85-1658-64ae-bc82-220a4d6213d5/859747478890_cover.jpg/600x600bb.jpg',
  'with you---ap dhillon': 'https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/5a/ac/00/5aac005f-9403-70e4-bce0-cf452017476e/197189606472.jpg/600x600bb.jpg',
  'insane---ap dhillon': 'https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/16/d6/94/16d6949f-6072-0b42-f88b-a61ffb129952/859747110851_cover.jpg/600x600bb.jpg',
  'dil nu---ap dhillon': 'https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/67/37/31/67373108-1018-da3f-7220-4515137e5e5e/859766525070_cover.jpg/600x600bb.jpg',
  'summer high---ap dhillon': 'https://is1-ssl.mzstatic.com/image/thumb/Music112/v4/50/0e/72/500e728f-d6d1-ec66-c994-9a98e1acb892/859764488018_cover.jpg/600x600bb.jpg',
  'majhail---ap dhillon': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/04/11/90/04119025-6a4f-337b-416b-89453f20cb12/5034644487823.jpg/600x600bb.jpg',
  'no love---shubh': 'https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/a7/b3/80/a7b380b9-9e29-1642-566e-d1ca4b920886/196776912972.jpg/600x600bb.jpg',
  'baller---shubh': 'https://is1-ssl.mzstatic.com/image/thumb/Music112/v4/e9/bd/93/e9bd9316-75a6-bc15-aebe-c737037bedf0/196925634489.jpg/600x600bb.jpg',
  'cheques---shubh': 'https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/dc/46/a9/dc46a9c9-794e-2d7a-1afb-97eb4ae0fff6/197188915704.jpg/600x600bb.jpg',
  'elevated---shubh': 'https://i.ytimg.com/vi/9CvwbW9UhJc/hqdefault.jpg',
  'still rollin---shubh': 'https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/dc/46/a9/dc46a9c9-794e-2d7a-1afb-97eb4ae0fff6/197188915704.jpg/600x600bb.jpg',
  'her---shubh': 'https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/dd/5a/56/dd5a567b-5531-8ef2-e7c4-2fd7c77e7d7f/197187463015.jpg/600x600bb.jpg',
  'one love---shubh': 'https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/48/4f/3c/484f3c19-fdab-1fa8-fdb4-c7de79852d12/197189603969.jpg/600x600bb.jpg',
  '295---sidhu moosewala': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/97/69/58/976958ae-725e-bd41-6755-f0921c697840/810063889609_cover.jpg/600x600bb.jpg',
  'so high---sidhu moosewala': 'https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/1b/6e/74/1b6e74cd-b93a-5dd9-e7a2-c7623df73d10/cover.jpg/600x600bb.jpg',
  'the last ride---sidhu moosewala': 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/db/2c/84/db2c84f2-f42f-af93-2709-6158995f9f72/810105712582_cover.jpg/600x600bb.jpg',
  'same beef---sidhu moosewala': 'https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/fe/c6/13/fec61345-4a34-8056-aff4-77d7ee71fabf/SameBeef_Inlay-_Itunes.jpg/600x600bb.jpg',
  'levels---sidhu moosewala': 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/37/ca/50/37ca5028-a2dc-975b-6366-6427c2b81761/5064089945930_cover.jpg/600x600bb.jpg',
  'old skool---prem dhillon': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/88/c2/f2/88c2f2d9-5def-9dc5-2e09-c01e748fa0ff/810059345621_cover.jpg/600x600bb.jpg',
  'pasoori---ali sethi': 'https://is1-ssl.mzstatic.com/image/thumb/Music116/v4/f3/f9/06/f3f906c3-79d5-ac9a-5fdd-262048f955f9/cover.jpg/600x600bb.jpg',
  'daku---chani nattan': 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/6d/0c/0a/6d0c0a1b-b50a-8320-f3fa-67eb450e54fc/ticket.sluflcmn.jpg/600x600bb.jpg',
  'mi amor---sharn': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/63/37/23/633723fa-a095-d5ed-794b-a2351c33851e/199350505591.jpg/600x600bb.jpg',

  // Hindi / Bollywood Romantic Hits
  'tum hi ho---arijit singh': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/bb/23/ee/bb23eeed-0c35-4f1d-2b11-485622777ae4/8902894353007_cover.jpg/600x600bb.jpg',
  'kesariya---arijit singh': 'https://is1-ssl.mzstatic.com/image/thumb/Music112/v4/9f/13/ca/9f13ca3b-e533-03e0-f19a-f0aaa774581d/196589311191.jpg/600x600bb.jpg',
  'raataan lambiyan---jubin nautiyal': 'https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/61/65/ae/6165aee9-8bb9-0bd4-02b0-5d0f1e6257a3/886449510238.jpg/600x600bb.jpg',
  'apna bana le---arijit singh': 'https://is1-ssl.mzstatic.com/image/thumb/Music122/v4/2e/0b/c0/2e0bc070-112f-a827-6ad8-6bc64f7caaff/840214460180.png/600x600bb.jpg',
  'shayad---arijit singh': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/4d/7c/9e/4d7c9e55-4ed7-ee60-83c8-49bc452227b3/886448257929.jpg/600x600bb.jpg',
  'channa mereya---arijit singh': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/bc/6e/4d/bc6e4d0c-adec-b431-7b60-16f5689f9664/886446201597.jpg/600x600bb.jpg',
  'kabira---tochi raina': 'https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/62/d6/74/62d67432-0670-631f-db6a-d4bac3adae4b/8902894353328_cover.jpg/600x600bb.jpg',
  'agar tum saath ho---alka yagnik': 'https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/cb/ac/67/cbac673a-9213-7118-bb4e-2440273afb03/8902894357470_cover.jpg/600x600bb.jpg',
  'kal ho naa ho---sonu nigam': 'https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/fb/82/da/fb82dab1-d0cd-714c-000c-6450774fd5d4/888880945587.jpg/600x600bb.jpg',
  'dil diyan gallan---atif aslam': 'https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/55/16/15/5516155a-733c-800c-1081-e5e982e8a603/849486091696_cover.jpg/600x600bb.jpg',
  'tujh mein rab dikhta hai---roop kumar rathod': 'https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/e5/7a/8b/e57a8bb7-8513-3bf9-8268-cc3062ae00df/849486008052_cover.jpg/600x600bb.jpg',
  'tera ban jaunga---akhil sachdeva': 'https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/f6/70/84/f6708434-0123-ff36-0ac3-7401e8cf0f94/8902894360807_cover.jpg/600x600bb.jpg',
  'gerua---arijit singh': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/dd/c8/ee/ddc8ee1d-baeb-0c8b-383f-1eb21bd172c2/886445593280.jpg/600x600bb.jpg',
  'hawayein---arijit singh': 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/41/aa/e3/41aae321-0a81-2762-e0eb-c60844109fe7/886446683584.jpg/600x600bb.jpg',
  'tum se hi---mohit chauhan': 'https://is1-ssl.mzstatic.com/image/thumb/Music124/v4/3d/c7/43/3dc74387-e7f4-2342-397c-4cf2037c69a5/8902894623223_cover.jpg/600x600bb.jpg',
  'jeena jeena---atif aslam': 'https://is1-ssl.mzstatic.com/image/thumb/Music221/v4/35/85/12/358512ee-128b-977f-40bc-669beb1bcc8d/196871079747.jpg/600x600bb.jpg',
  'pee loon---mohit chauhan': 'https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/f3/d9/23/f3d92398-118c-10c9-2ef8-5f28cff344c2/8902894688512_cover.jpg/600x600bb.jpg',
  'satranga---arijit singh': 'https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/db/ad/5e/dbad5e8b-0bee-d962-92d4-021c90e375ac/8902894362092_cover.jpg/600x600bb.jpg',
  'mast magan---arijit singh': 'https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/e1/1b/83/e11b8398-0089-cfb1-f998-16125b3f17c4/8902894355612_cover.jpg/600x600bb.jpg',
  'khairiyat---arijit singh': 'https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/da/5a/14/da5a1435-fc2a-5ab9-667f-a9bf2daa46f4/8902894360937_cover.jpg/600x600bb.jpg',

  // Western & Acoustic Hits
  'acoustic breeze---benjamin tissot': 'https://is1-ssl.mzstatic.com/image/thumb/Video/ae/99/45/mzi.ckzdtpsh.jpg/600x600bb.jpg',
  'creative minds---benjamin tissot': 'https://is1-ssl.mzstatic.com/image/thumb/Music128/v4/c0/c4/20/c0c42093-6f92-5670-e918-1495f0f417f5/artwork.jpg/600x600bb.jpg',
  'cruel summer---taylor swift': 'https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/49/3d/ab/493dab54-f920-9043-6181-80993b8116c9/19UMGIM53909.rgb.jpg/600x600bb.jpg',
  'blinding lights---the weeknd': 'https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/6f/bc/e6/6fbce6c4-c38c-72d8-4fd0-66cfff32f679/20UMGIM12176.rgb.jpg/600x600bb.jpg',
  'as it was---harry styles': 'https://is1-ssl.mzstatic.com/image/thumb/Music126/v4/2a/19/fb/2a19fb85-2f70-9e44-f2a9-82abe679b88e/886449990061.jpg/600x600bb.jpg',
  'perfect---ed sheeran': 'https://is1-ssl.mzstatic.com/image/thumb/Music115/v4/15/e6/e8/15e6e8a4-4190-6a8b-86c3-ab4a51b88288/190295851286.jpg/600x600bb.jpg',
  'stay---the kid laroi': 'https://is1-ssl.mzstatic.com/image/thumb/Music125/v4/89/59/6a/89596ab9-fa3c-8d08-4d95-a6450fa2013c/886449400515.jpg/600x600bb.jpg',
  'birds of a feather---billie eilish': 'https://is1-ssl.mzstatic.com/image/thumb/Music211/v4/92/9f/69/929f69f1-9977-3a44-d674-11f70c852d1b/24UMGIM36186.rgb.jpg/600x600bb.jpg',
};

// Global artwork cache across the session
const artworkMemoryCache = new Map<string, string>();

if (typeof window !== 'undefined') {
  try {
    const saved = localStorage.getItem('ais_artwork_cache');
    if (saved) {
      const parsed = JSON.parse(saved);
      for (const [k, v] of Object.entries(parsed)) {
        if (typeof v === 'string') artworkMemoryCache.set(k, v);
      }
    }
  } catch (e) {
    // Ignore
  }
}

function persistArtwork(key: string, url: string) {
  artworkMemoryCache.set(key, url);
  if (typeof window !== 'undefined') {
    try {
      const obj: Record<string, string> = {};
      artworkMemoryCache.forEach((v, k) => {
        obj[k] = v;
      });
      localStorage.setItem('ais_artwork_cache', JSON.stringify(obj));
    } catch (e) {
      // Ignore
    }
  }
}

export function getKnownArtwork(title?: string, artist?: string): string | null {
  if (!title) return null;
  const t = title.trim().toLowerCase();
  const a = (artist || '').trim().toLowerCase();

  // 1. Direct memory cache
  const fullKey = `${t}---${a}`;
  if (artworkMemoryCache.has(fullKey)) return artworkMemoryCache.get(fullKey)!;

  // 2. Exact match in verified map
  if (VERIFIED_ARTWORK_MAP[fullKey]) return VERIFIED_ARTWORK_MAP[fullKey];

  // 3. Match by song title and partial artist
  for (const [key, url] of Object.entries(VERIFIED_ARTWORK_MAP)) {
    const [kTitle, kArtist] = key.split('---');
    if (t.includes(kTitle) || kTitle.includes(t)) {
      if (!a || !kArtist || a.includes(kArtist) || kArtist.includes(a)) {
        return url;
      }
    }
  }

  return null;
}

export interface SongImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  song?: Partial<Song> | null;
  coverUrl?: string;
  title?: string;
  artist?: string;
  youtubeId?: string;
  fallbackIconSize?: number;
  className?: string;
  alt?: string;
}

export function SongImage({
  song,
  coverUrl: directCoverUrl,
  title: directTitle,
  artist: directArtist,
  youtubeId: directYoutubeId,
  className = '',
  alt = '',
  fallbackIconSize = 24,
  ...props
}: SongImageProps) {
  const title = song?.title || directTitle || '';
  const artist = song?.artist || directArtist || '';
  const initialCover = song?.coverUrl || directCoverUrl || '';
  const ytId = song?.youtubeId || directYoutubeId || '';

  const cacheKey = `${title.trim().toLowerCase()}---${artist.trim().toLowerCase()}`;

  // Check if we have verified artwork first
  const knownArtwork = getKnownArtwork(title, artist);

  const getInitialSource = () => {
    // If the provided coverUrl is a generic unsplash photo, discard it and use known artwork
    const isUnsplash = initialCover.includes('images.unsplash.com');
    if (isUnsplash && knownArtwork) {
      return knownArtwork;
    }
    if (knownArtwork) {
      return knownArtwork;
    }
    if (initialCover && !isUnsplash) {
      return initialCover;
    }
    if (ytId) {
      return `https://i.ytimg.com/vi/${ytId}/hqdefault.jpg`;
    }
    return '';
  };

  const [currentSrc, setCurrentSrc] = useState<string>(getInitialSource);
  const [hasError, setHasError] = useState(false);
  const [retryStage, setRetryStage] = useState<number>(0);

  useEffect(() => {
    const freshSrc = getInitialSource();
    if (freshSrc) {
      setCurrentSrc(freshSrc);
      setHasError(false);
      setRetryStage(0);
    } else if (title) {
      // Proactively fetch actual artwork from server or iTunes
      fetchActualArtwork();
    }
  }, [title, artist, initialCover, ytId]);

  const fetchActualArtwork = () => {
    if (!title) return;
    // 1. Try server endpoint
    fetch(`/api/song-artwork?title=${encodeURIComponent(title)}&artist=${encodeURIComponent(artist)}`)
      .then(res => res.json())
      .then(data => {
        if (data?.artwork) {
          persistArtwork(cacheKey, data.artwork);
          setCurrentSrc(data.artwork);
          setHasError(false);
        } else if (ytId) {
          setCurrentSrc(`https://i.ytimg.com/vi/${ytId}/hqdefault.jpg`);
        }
      })
      .catch(() => {
        // Fallback to direct itunes query
        fetch(`https://itunes.apple.com/search?term=${encodeURIComponent(title + ' ' + artist)}&entity=song&limit=1`)
          .then(res => res.json())
          .then(data => {
            if (data.results && data.results[0] && data.results[0].artworkUrl100) {
              const art = data.results[0].artworkUrl100.replace('100x100bb.jpg', '600x600bb.jpg').replace('100x100bb.png', '600x600bb.png');
              persistArtwork(cacheKey, art);
              setCurrentSrc(art);
              setHasError(false);
            } else if (ytId) {
              setCurrentSrc(`https://i.ytimg.com/vi/${ytId}/hqdefault.jpg`);
            } else {
              setHasError(true);
            }
          })
          .catch(() => {
            if (ytId) {
              setCurrentSrc(`https://i.ytimg.com/vi/${ytId}/hqdefault.jpg`);
            } else {
              setHasError(true);
            }
          });
      });
  };

  const handleImageError = () => {
    // Stage 0: Check known artwork dictionary
    if (knownArtwork && currentSrc !== knownArtwork) {
      setCurrentSrc(knownArtwork);
      return;
    }

    // Stage 1: Try official YouTube video thumbnail
    if (retryStage === 0 && ytId) {
      setRetryStage(1);
      setCurrentSrc(`https://i.ytimg.com/vi/${ytId}/hqdefault.jpg`);
      return;
    }

    // Stage 2: Fetch actual artwork dynamically
    if (retryStage <= 1 && title) {
      setRetryStage(2);
      fetchActualArtwork();
      return;
    }

    // If all recovery methods failed, show high-aesthetic vinyl card placeholder
    setHasError(true);
  };

  if (hasError || !currentSrc) {
    return (
      <div 
        className={`bg-gradient-to-br from-neutral-800 via-neutral-900 to-black flex flex-col items-center justify-center text-white/80 overflow-hidden relative select-none ${className}`}
      >
        <div className="absolute inset-0 bg-radial-gradient from-white/10 to-transparent pointer-events-none" />
        <Music size={fallbackIconSize} className="text-white/70 mb-1" />
        {title && (
          <span className="text-[10px] font-semibold text-center px-2 truncate max-w-full text-white/90">
            {title}
          </span>
        )}
      </div>
    );
  }

  return (
    <img
      src={currentSrc}
      alt={alt || title || 'Song artwork'}
      className={className}
      onError={handleImageError}
      loading="lazy"
      {...props}
    />
  );
}
