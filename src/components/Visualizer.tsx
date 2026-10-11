import React, { useEffect, useRef } from 'react';

export function Visualizer({ analyzer }: { analyzer: any }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!analyzer || !canvasRef.current) return;
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // Auto-resize canvas
    const resize = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    resize();
    window.addEventListener('resize', resize);
    
    const bufferLength = analyzer.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    
    let animationId: number;
    
    const draw = () => {
      animationId = requestAnimationFrame(draw);
      
      analyzer.getByteFrequencyData(dataArray);
      
      const width = canvas.width;
      const height = canvas.height;
      
      ctx.clearRect(0, 0, width, height);
      
      // Let's draw a nice radial spectrum or bar spectrum centered
      const barWidth = (width / bufferLength) * 2.5;
      let x = 0;
      
      for (let i = 0; i < bufferLength; i++) {
        const barHeight = (dataArray[i] / 255) * height;
        
        const gradient = ctx.createLinearGradient(0, height, 0, 0);
        gradient.addColorStop(0, 'rgba(202, 90, 44, 0.4)');
        gradient.addColorStop(1, 'rgba(202, 90, 44, 1)');
        
        ctx.fillStyle = gradient;
        // Centered vertically
        ctx.fillRect(x, (height - barHeight) / 2, barWidth, barHeight);
        
        x += barWidth + 1;
      }
    };
    
    draw();
    
    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resize);
    };
  }, [analyzer]);

  return (
    <canvas 
      ref={canvasRef} 
      className="w-full h-full"
    />
  );
}
