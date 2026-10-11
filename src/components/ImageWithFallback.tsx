import { useState, ImgHTMLAttributes } from 'react';

interface ImageWithFallbackProps extends ImgHTMLAttributes<HTMLImageElement> {
  fallbackSrc?: string;
  src?: string;
  alt?: string;
}

export function ImageWithFallback({ 
  src, 
  fallbackSrc = 'https://images.unsplash.com/photo-1618519764611-bd0877e2e4f7?q=80&w=2667&auto=format&fit=crop', 
  alt, 
  ...props 
}: ImageWithFallbackProps) {
  const [imgSrc, setImgSrc] = useState(src);

  return (
    <img
      {...props}
      src={imgSrc}
      alt={alt}
      onError={() => {
        if (imgSrc !== fallbackSrc) {
          setImgSrc(fallbackSrc);
        }
      }}
    />
  );
}
