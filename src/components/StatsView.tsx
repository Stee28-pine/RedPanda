import React, { useMemo } from 'react';
import { motion } from 'motion/react';
import { Clock, Music, Mic2, Disc, BarChart3 } from 'lucide-react';
import { ListeningStats } from '../hooks/useListeningStats';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export function StatsView({ stats }: { stats: ListeningStats }) {
  const topArtists = Object.entries(stats.artistPlays || {}).sort((a, b) => b[1] - a[1]).slice(0, 5);
  const topGenres = Object.entries(stats.genrePlays || {}).sort((a, b) => b[1] - a[1]).slice(0, 5);
  const topSongs = Object.entries(stats.songPlays || {}).sort((a, b) => b[1] - a[1]).slice(0, 5);
  const totalHours = (stats.totalTimeSeconds / 3600).toFixed(1);

  const chartData = useMemo(() => {
    if (!stats.dailyActivity) return [];
    
    // Sort dates
    const dates = Object.keys(stats.dailyActivity).sort();
    
    // Create last 7 days empty structure if not enough data
    const last7Days = [];
    const today = new Date();
    
    for (let i = 6; i >= 0; i--) {
       const d = new Date(today);
       d.setDate(today.getDate() - i);
       const dateStr = d.toISOString().split('T')[0];
       
       // Format for display (e.g. "Mon", "Tue")
       const displayLabel = d.toLocaleDateString('en-US', { weekday: 'short' });
       
       const seconds = stats.dailyActivity[dateStr] || 0;
       last7Days.push({
          date: dateStr,
          label: displayLabel,
          minutes: Math.round(seconds / 60)
       });
    }
    return last7Days;
  }, [stats.dailyActivity]);

  return (
    <div className="h-full overflow-y-auto hide-scrollbar pb-32">
      <div className="p-8 max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8">Your Listening Stats</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
          <StatCard icon={<Clock className="text-[#fe5f64]" />} label="Total Time" value={`${totalHours} hrs`} />
          <StatCard icon={<Mic2 className="text-[#fe5f64]" />} label="Top Artist" value={topArtists[0]?.[0] || 'N/A'} />
          <StatCard icon={<Disc className="text-[#fe5f64]" />} label="Top Genre" value={topGenres[0]?.[0] || 'N/A'} />
          <StatCard icon={<Music className="text-[#fe5f64]" />} label="Top Song" value={topSongs[0]?.[0] || 'N/A'} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          <div className="lg:col-span-2 bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
             <h3 className="text-lg font-bold mb-6 flex items-center gap-2"><BarChart3 size={16} /> Daily Activity (Minutes)</h3>
             <div className="h-[250px] w-full">
                <ResponsiveContainer width="100%" height="100%">
                   <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                      <XAxis dataKey="label" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} dy={10} />
                      <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} />
                      <Tooltip 
                         cursor={{ fill: '#F3F4F6' }}
                         contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                         labelStyle={{ color: '#9CA3AF', fontWeight: '500', marginBottom: '4px' }}
                      />
                      <Bar dataKey="minutes" fill="#fe5f64" radius={[4, 4, 0, 0]} maxBarSize={40} />
                   </BarChart>
                </ResponsiveContainer>
             </div>
          </div>
          
          <div className="lg:col-span-1">
             <ListCard title="Top Artists" items={topArtists} icon={<Mic2 size={16} />} />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <ListCard title="Top Genres" items={topGenres} icon={<Disc size={16} />} />
          <ListCard title="Top Songs" items={topSongs} icon={<Music size={16} />} />
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value }: { icon: React.ReactNode, label: string, value: string }) {
  return (
    <motion.div whileHover={{ scale: 1.02 }} className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center gap-4">
      <div className="w-12 h-12 rounded-full bg-orange-50 flex items-center justify-center">
        {icon}
      </div>
      <div>
        <div className="text-sm text-gray-500 font-medium">{label}</div>
        <div className="text-xl font-bold truncate">{value}</div>
      </div>
    </motion.div>
  );
}

function ListCard({ title, items, icon }: { title: string, items: [string, number][], icon: React.ReactNode }) {
  return (
    <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 h-full">
      <h3 className="text-lg font-bold mb-4 flex items-center gap-2">{icon} {title}</h3>
      <div className="space-y-4">
        {items.length === 0 ? (
          <div className="text-sm text-gray-400">No data yet</div>
        ) : items.map(([name, count], index) => (
          <div key={name} className="flex items-center justify-between group">
            <div className="flex items-center gap-3 min-w-0">
              <span className="text-gray-400 text-sm font-medium w-4">{index + 1}</span>
              <span className="font-semibold text-gray-800 truncate">{name}</span>
            </div>
            <span className="text-xs text-gray-400 font-medium whitespace-nowrap">{count} plays</span>
          </div>
        ))}
      </div>
    </div>
  );
}
