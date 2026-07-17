"use client";

import { useState, useRef } from "react";

export default function Home() {
  const [contentFile, setContentFile] = useState(null);
  const [styleFile, setStyleFile] = useState(null);
  const [contentPreview, setContentPreview] = useState(null);
  const [stylePreview, setStylePreview] = useState(null);

  const [steps, setSteps] = useState(150);
  const [styleWeight, setStyleWeight] = useState(1000000);
  const [imageSize, setImageSize] = useState(192);

  const [loading, setLoading] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const [resultUrl, setResultUrl] = useState(null);
  const [error, setError] = useState(null);

  const contentInputRef = useRef(null);
  const styleInputRef = useRef(null);
  const timerRef = useRef(null);

  const handleContentChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setContentFile(file);
    setContentPreview(URL.createObjectURL(file));
    setResultUrl(null);
    setError(null);
  };

  const handleStyleChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setStyleFile(file);
    setStylePreview(URL.createObjectURL(file));
    setResultUrl(null);
    setError(null);
  };

  const handleGenerate = async () => {
    if (!contentFile || !styleFile) {
      setError("Both a content image and a style image are required.");
      return;
    }

    setLoading(true);
    setError(null);
    setResultUrl(null);
    setElapsed(0);

    timerRef.current = setInterval(() => {
      setElapsed((prev) => prev + 1);
    }, 1000);

    try {
      const formData = new FormData();
      formData.append("content_image", contentFile);
      formData.append("style_image", styleFile);
      formData.append("steps", steps);
      formData.append("style_weight", styleWeight);
      formData.append("image_size", imageSize);

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

      const response = await fetch(`${apiUrl}/generate`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Generation failed. Please try again.");
      }

      const blob = await response.blob();
      setResultUrl(URL.createObjectURL(blob));
    } catch (err) {
      setError(err.message);
    } finally {
      clearInterval(timerRef.current);
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  return (
    <main className="min-h-screen bg-bg bg-grid-texture">
      {/* hero */}
      <div className="border-b-4 border-red px-8 sm:px-16 pt-12 pb-8 relative overflow-hidden">
        <div
          className="absolute right-[-2rem] top-[-2rem] font-display pointer-events-none select-none"
          style={{ fontSize: "18rem", color: "rgba(255,45,0,0.04)", lineHeight: 1 }}
        >
          ART
        </div>
        <p className="font-mono text-[0.7rem] text-red tracking-[0.3rem] uppercase mb-2 border-l-2 border-red pl-3">
          Neural Style Transfer Engine · Vol. 01
        </p>
        <h1 className="font-display text-ink leading-[0.85] text-[5rem] sm:text-[7rem] lg:text-[9rem] tracking-wide">
          PICASS
          <span className="text-red block">IFY</span>
        </h1>
        <p className="font-body font-light text-[1.2rem] text-muted tracking-[0.15em] uppercase mt-3 pt-4 border-t border-line max-w-xl">
          Upload. Transmute. Collect your masterpiece.
        </p>
      </div>

      {/* ticker */}
      <div className="bg-red py-1.5 px-8 overflow-hidden">
        <span className="ticker-text font-body font-semibold text-[0.8rem] tracking-[0.25em] text-bg uppercase">
          NEURAL STYLE TRANSFER &nbsp;·&nbsp; VGG19 ARCHITECTURE &nbsp;·&nbsp;
          GRAM MATRIX &nbsp;·&nbsp; CONTENT LOSS &nbsp;·&nbsp; STYLE LOSS &nbsp;·&nbsp;
          PYTORCH ENGINE &nbsp;·&nbsp; UPLOAD YOUR PHOTO &nbsp;·&nbsp;
          CHOOSE YOUR STYLE &nbsp;·&nbsp; GENERATE ART &nbsp;·&nbsp;
          NEURAL STYLE TRANSFER &nbsp;·&nbsp; VGG19 ARCHITECTURE &nbsp;·&nbsp;
          GRAM MATRIX &nbsp;·&nbsp; CONTENT LOSS &nbsp;·&nbsp; STYLE LOSS &nbsp;·&nbsp;
          PYTORCH ENGINE &nbsp;·&nbsp; UPLOAD YOUR PHOTO &nbsp;·&nbsp;
          CHOOSE YOUR STYLE &nbsp;·&nbsp; GENERATE ART &nbsp;·&nbsp;
        </span>
      </div>

      <div className="px-8 sm:px-16 py-10">
        {/* section 01 - input */}
        <p className="font-mono text-[0.65rem] text-red tracking-[0.4rem] uppercase mb-4 flex items-center gap-4">
          01 — Input
          <span className="flex-1 h-px bg-line" />
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* content upload */}
          <label className="border-2 border-line bg-panel hover:border-red transition-colors cursor-pointer block">
            <div className="bg-panel-alt border-b border-line px-5 py-3 flex justify-between items-center">
              <div>
                <div className="font-body font-extrabold text-[1.3rem] tracking-wide uppercase text-ink">
                  The Subject
                </div>
                <div className="font-mono text-[0.65rem] text-faint uppercase tracking-wider">
                  Your photograph
                </div>
              </div>
              <div className="font-display text-red text-[2.8rem] leading-none">01</div>
            </div>
            <div className="p-5">
              <input
                ref={contentInputRef}
                type="file"
                accept="image/*"
                onChange={handleContentChange}
                className="hidden"
              />
              {contentPreview ? (
                <img
                  src={contentPreview}
                  alt="Content"
                  className="w-full h-56 object-cover border border-line"
                />
              ) : (
                <div className="w-full h-56 flex items-center justify-center font-mono text-[0.7rem] text-faint uppercase tracking-wider border border-dashed border-line">
                  Click to upload
                </div>
              )}
            </div>
          </label>

          {/* style upload */}
          <label className="border-2 border-line bg-panel hover:border-red transition-colors cursor-pointer block">
            <div className="bg-panel-alt border-b border-line px-5 py-3 flex justify-between items-center">
              <div>
                <div className="font-body font-extrabold text-[1.3rem] tracking-wide uppercase text-ink">
                  The Style
                </div>
                <div className="font-mono text-[0.65rem] text-faint uppercase tracking-wider">
                  Your painting / artwork
                </div>
              </div>
              <div className="font-display text-red text-[2.8rem] leading-none">02</div>
            </div>
            <div className="p-5">
              <input
                ref={styleInputRef}
                type="file"
                accept="image/*"
                onChange={handleStyleChange}
                className="hidden"
              />
              {stylePreview ? (
                <img
                  src={stylePreview}
                  alt="Style"
                  className="w-full h-56 object-cover border border-line"
                />
              ) : (
                <div className="w-full h-56 flex items-center justify-center font-mono text-[0.7rem] text-faint uppercase tracking-wider border border-dashed border-line">
                  Click to upload
                </div>
              )}
            </div>
          </label>
        </div>

        {/* settings */}
        <div className="bg-panel border-2 border-line border-l-4 border-l-red p-8 my-10">
          <div className="font-display text-[2rem] text-ink tracking-wide">Parameters</div>
          <div className="font-mono text-[0.65rem] text-faint tracking-[0.2em] uppercase mb-6">
            Configure the style transfer engine
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
            <div>
              <label className="font-mono text-[0.7rem] text-muted tracking-wide uppercase block mb-2">
                Iterations: {steps}
              </label>
              <input
                type="range"
                min="50"
                max="300"
                step="10"
                value={steps}
                onChange={(e) => setSteps(Number(e.target.value))}
                className="w-full accent-red"
              />
              <p className="font-mono text-[0.6rem] text-faint mt-1">
                Fewer = faster, more = more refined
              </p>
            </div>

            <div>
              <label className="font-mono text-[0.7rem] text-muted tracking-wide uppercase block mb-2">
                Style Strength
              </label>
              <select
                value={styleWeight}
                onChange={(e) => setStyleWeight(Number(e.target.value))}
                className="w-full bg-panel-alt border border-line text-ink font-mono text-[0.75rem] px-3 py-2"
              >
                <option value={100000}>Subtle</option>
                <option value={500000}>Moderate</option>
                <option value={1000000}>Strong</option>
                <option value={5000000}>Intense</option>
                <option value={10000000}>Max</option>
              </select>
            </div>

            <div>
              <label className="font-mono text-[0.7rem] text-muted tracking-wide uppercase block mb-2">
                Canvas Size
              </label>
              <select
                value={imageSize}
                onChange={(e) => setImageSize(Number(e.target.value))}
                className="w-full bg-panel-alt border border-line text-ink font-mono text-[0.75rem] px-3 py-2"
              >
                <option value={128}>128 × 128 (fastest)</option>
                <option value={192}>192 × 192 (balanced)</option>
                <option value={256}>256 × 256 (slow)</option>
              </select>
            </div>
          </div>
        </div>

        {/* section 02 - generate */}
        <p className="font-mono text-[0.65rem] text-red tracking-[0.4rem] uppercase mb-4 flex items-center gap-4">
          02 — Generate
          <span className="flex-1 h-px bg-line" />
        </p>

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="w-full bg-red text-bg font-display text-[1.5rem] tracking-[0.3rem] uppercase py-4 transition-all hover:bg-ink hover:-translate-y-1 hover:shadow-[6px_6px_0px_#ff2d00] active:translate-y-0 active:shadow-none disabled:opacity-50 disabled:hover:translate-y-0 disabled:hover:shadow-none cursor-pointer"
        >
          {loading ? "Generating..." : "Execute Style Transfer"}
        </button>

        {error && (
          <p className="font-mono text-[0.75rem] text-red mt-4 uppercase tracking-wide">
            Error — {error}
          </p>
        )}

        {/* loading state */}
        {loading && (
          <div className="mt-8 text-center">
            <div className="font-display text-[2.5rem] text-ink tracking-wide shimmer">
              GENERATING ARTWORK
            </div>
            <p className="font-mono text-[0.75rem] text-faint mt-2 uppercase tracking-wider">
              Elapsed: {formatTime(elapsed)} — this typically takes 1–4 minutes.
              Please don't close this tab.
            </p>
          </div>
        )}

        {/* result */}
        {resultUrl && (
          <div className="mt-10">
            <p className="font-mono text-[0.65rem] text-red tracking-[0.4rem] uppercase mb-4 flex items-center gap-4">
              03 — Output
              <span className="flex-1 h-px bg-line" />
            </p>
            <img
              src={resultUrl}
              alt="Generated artwork"
              className="w-full border border-line"
            />
            <a
              href={resultUrl}
              download="picassify_artwork.png"
              className="mt-4 block text-center border-2 border-red text-red font-mono text-[0.8rem] tracking-[0.2em] uppercase py-3 hover:bg-red hover:text-bg transition-colors"
            >
              Download Artwork
            </a>
          </div>
        )}
      </div>

      {/* footer */}
      <div className="border-t-4 border-red px-8 sm:px-16 py-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mt-10">
        <div className="font-display text-[1.5rem] text-ink tracking-wide">PICASSIFY</div>
        <div className="font-mono text-[0.65rem] text-faint text-left sm:text-right leading-relaxed">
          BUILT BY ALI FARAZ<br />
          PYTORCH · VGG19 · FASTAPI · NEXT.JS<br />
          NEURAL STYLE TRANSFER · GATYS ET AL. 2015
        </div>
      </div>
    </main>
  );
}