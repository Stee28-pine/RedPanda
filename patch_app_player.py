import re

with open('src/App.tsx', 'r') as f:
    content = f.read()

old_react_player = """        <div className="absolute opacity-[0.01] pointer-events-none -z-10 w-[200px] h-[200px] overflow-hidden">
          <ReactPlayer
            ref={playerRef}
            url={nowPlayingUrl || ""}
            playing={isPlaying}
            volume={volume * crossfadeVolume}
            config={{ youtube: { playerVars: { playsinline: 1, autoplay: 1 } }, file: { forceAudio: true, attributes: { crossOrigin: 'anonymous' } } }}"""

new_react_player = """        <div className="absolute opacity-[0.01] pointer-events-none -z-10 w-[200px] h-[200px] overflow-hidden">
          <ReactPlayer
            ref={playerRef}
            url={nowPlayingUrl || ""}
            playing={isPlaying}
            playbackRate={playbackRate}
            volume={volume * crossfadeVolume}
            config={{ youtube: { playerVars: { playsinline: 1, autoplay: 1 } }, file: { forceAudio: true, attributes: { crossOrigin: 'anonymous' } } }}"""

content = content.replace(old_react_player, new_react_player)

with open('src/App.tsx', 'w') as f:
    f.write(content)
print("Patched App.tsx with playbackRate")
