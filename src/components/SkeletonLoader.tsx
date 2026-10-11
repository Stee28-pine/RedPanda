export function SkeletonHero() {
  return (
    <div className="relative w-full h-[75vh] min-h-[500px] bg-[#111] animate-pulse">
      <div className="absolute inset-0 bg-gradient-to-r from-[#000] via-[#000]/60 to-transparent w-3/4" />
      <div className="absolute inset-0 bg-gradient-to-t from-[#000] via-[#000]/20 to-transparent" />

      <div className="absolute bottom-0 left-0 p-12 md:p-16 lg:p-24 w-full md:max-w-2xl flex flex-col justify-end gap-4">
        <div className="w-1/3 h-4 bg-white/10 rounded-full" />
        <div className="w-3/4 h-16 bg-white/10 rounded-2xl my-2" />
        <div className="flex items-center gap-4 mt-2">
          <div className="w-40 h-[52px] bg-white/20 rounded-full" />
          <div className="w-32 h-[52px] bg-white/10 rounded-full" />
        </div>
      </div>
    </div>
  );
}

export function SkeletonRow() {
  return (
    <div className="w-full mb-8 animate-pulse">
      <div className="px-12 md:px-16 lg:px-24 mb-3">
        <div className="w-48 h-8 bg-white/10 rounded-lg" />
      </div>

      <div className="flex gap-6 overflow-hidden px-12 md:px-16 lg:px-24 pb-12 pt-4">
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="flex-none w-[280px] md:w-[320px] aspect-video bg-[#1A1A1A] rounded-[12px]" />
        ))}
      </div>
    </div>
  );
}
