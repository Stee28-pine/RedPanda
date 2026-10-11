import { useState, useCallback, useRef } from 'react';

export function useVoiceSearch(onSearch: (query: string) => void) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const transcriptRef = useRef('');

  const startListening = useCallback(() => {
    if (!('webkitSpeechRecognition' in window)) {
      console.error("Voice search is not supported in this browser.");
      return;
    }

    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsListening(true);
      setTranscript('');
      transcriptRef.current = '';
    };

    recognition.onresult = (event: any) => {
      let currentTranscript = '';
      for (let i = event.resultIndex; i < event.results.length; ++i) {
        currentTranscript += event.results[i][0].transcript;
      }
      setTranscript(currentTranscript);
      transcriptRef.current = currentTranscript;
    };

    recognition.onerror = (event: any) => {
      console.error(event.error);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
      if (transcriptRef.current.trim()) {
        onSearch(transcriptRef.current.trim());
      }
    };

    recognition.start();

    return () => {
      recognition.stop();
    };
  }, [onSearch]);

  const stopListening = useCallback(() => {
    setIsListening(false);
  }, []);

  return { isListening, transcript, startListening, stopListening };
}
