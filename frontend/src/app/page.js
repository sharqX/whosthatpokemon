"use client";
import AnimatedContent from '../components/AnimatedContent'
import DecryptedText from '../components/DecryptedText';
import { useEffect, useState, useRef, useCallback } from 'react';

export default function Home() {
  const [data, setData] = useState({
    id: '',
    type: '',
    height: '',
    weight: '',
    hint: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Works for both shapes: array vs object, Capitalized vs lowercase keys
  const normalize = (raw) => {
    const item = Array.isArray(raw) ? raw[0] : raw;
    if (!item || typeof item !== 'object') {
      return { id: '', type: '', height: '', weight: '', hint: '' };
    }

    const get = (lower, upper) => (item[lower] ?? item[upper] ?? '');

    return {
      id: get('id', 'Id'),
      type: get('type', 'Type'),
      height: get('height', 'Height'),
      weight: get('weight', 'Weight'),
      hint: get('hint', 'Hint'),
    };
  };

  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      console.log('Fetching from http://localhost:8000/...');
      const res = await fetch('http://localhost:8000/', { cache: 'no-store' });
      console.log('Response status:', res.status, res.statusText);
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
      const json = await res.json();
      console.log('Received data:', json);
      const normalized = normalize(json);
      console.log('Normalized data:', normalized);
      setData(normalized);
    } catch (err) {
      console.error('Fetch error:', err);
      setError(err?.message || 'Failed to fetch');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let mounted = true;
    (async () => {
      try {
        setLoading(true);
        setError(null);
        const res = await fetch('http://localhost:8000/', { cache: 'no-store' });
        if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
        const json = await res.json();
        if (mounted) setData(normalize(json));
      } catch (err) {
        if (mounted) setError(err?.message || 'Failed to fetch');
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => { mounted = false; };
  }, []); // don't include normalize here to avoid re-runs

  return (
    <>
      <div className="page-title">
        <DecryptedText
          text="Who's that Pokémon?"
          animateOn="both"
          revealDirection="start"
          speed={80}
        />
      </div>

      <AnimatedContent
        distance={500}
        direction="vertical"
        reverse={false}
        duration={1.0}
        ease="power3.out"
        initialOpacity={0}
        animateOpacity
        scale={1}
        threshold={0.2}
        delay={0.15}
      >
        <div className="card">
          <form className="card-form" onSubmit={(e) => e.preventDefault()}>
            <div className="card-top">
              <label className="field">
                <span className="label">ID:</span>
                <div className="editable">
                  {loading ? 'Loading...' : data.id}
                </div>
              </label>

              {error && (
                <div style={{ color: '#fca5a5', marginTop: 8 }}>
                  <div style={{ fontSize: 12 }}>Error: {error}</div>
                  <button
                    type="button"
                    onClick={fetchData}
                    disabled={loading}
                    style={{ marginTop: 6, padding: '6px 8px', fontSize: 12 }}
                  >
                    {loading ? 'Retrying...' : 'Retry'}
                  </button>
                </div>
              )}
            </div>

            <div className="card-bottom">
              <label className="field">
                <span className="label">Type:</span>
                <div className="editable">
                  {loading ? '' : data.type}
                </div>
              </label>

              <label className="field">
                <span className="label">Height:</span>
                <div className="editable">
                  {loading ? '' : data.height}
                </div>
              </label>

              <label className="field">
                <span className="label">Weight:</span>
                <div className="editable">
                  {loading ? '' : data.weight}
                </div>
              </label>

              <label className="field">
                <span className="label">Hint:</span>
                <div className="editable">
                  {loading ? '' : data.hint}
                </div>
              </label>
            </div>
          </form>
        </div>
      </AnimatedContent>
    </>
  );
}
