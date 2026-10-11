import re

with open('src/components/HomeView.tsx', 'r') as f:
    content = f.read()

old_markup = """        <motion.section 
          className="mb-12"
          initial="hidden"
          animate="show"
          variants={{
            hidden: { opacity: 0 },
            show: { opacity: 1, transition: { staggerChildren: 0.08 } }
          }}
        >
          <h2 className="text-[22px] font-bold text-gray-900 mb-5 tracking-tight">Recommended for You</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-6">
            {recommendedForYou.map((song) => (
              <motion.div 
                key={song.id}
                variants={{
                  hidden: { opacity: 0, y: 15, scale: 0.95 },
                  show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
                }}
                whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
                className="cursor-pointer group relative"
                onClick={() => onPlaySong?.(song, { songs: recommendedForYou })}
              >"""

new_markup = """        <motion.section 
          className="mb-12"
          initial="hidden"
          animate="show"
          variants={{
            hidden: { opacity: 0 },
            show: { opacity: 1, transition: { staggerChildren: 0.08 } }
          }}
        >
          <h2 className="text-[22px] font-bold text-gray-900 mb-5 tracking-tight">For You</h2>
          <div className="flex overflow-x-auto gap-4 md:gap-6 pb-4 snap-x [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
            {recommendedForYou.map((song) => (
              <motion.div 
                key={song.id}
                variants={{
                  hidden: { opacity: 0, y: 15, scale: 0.95 },
                  show: { opacity: 1, y: 0, scale: 1, transition: { type: "spring", stiffness: 200, damping: 20 } }
                }}
                whileHover={{ y: -6, scale: 1.03, transition: { duration: 0.2 } }}
                className="cursor-pointer group relative min-w-[140px] md:min-w-[180px] w-[140px] md:w-[180px] snap-start shrink-0"
                onClick={() => onPlaySong?.(song, { songs: recommendedForYou })}
              >"""

content = content.replace(old_markup, new_markup)

with open('src/components/HomeView.tsx', 'w') as f:
    f.write(content)

