import { useState, ImgHTMLAttributes } from 'react';

export interface SafeImageProps extends ImgHTMLAttributes<HTMLImageElement> {
  fallbackSrc?: string;
  src?: string;
  alt?: string;
  className?: string;
  loading?: "eager" | "lazy";
}

export function SafeImage({ 
  src, 
  fallbackSrc = 'https://images.unsplash.com/photo-1618519764611-bd0877e2e4f7?q=80&w=2667&auto=format&fit=crop', 
  className, 
  alt,
  ...props 
}: SafeImageProps) {
  const [error, setError] = useState(false);

  return (
    <img
      src={error || !src ? fallbackSrc : src}
      alt={alt || ''}
      className={className}
      onError={() => setError(true)}
      {...props}
    />
  );
}
