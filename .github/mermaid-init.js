/**
 * Mermaid initialization script for md-to-pdf
 * This script initializes Mermaid and renders all diagrams before PDF generation
 */

// Wait for page to load
if (typeof mermaid !== 'undefined') {
  mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose',
    fontFamily: 'Noto Sans CJK JP, sans-serif',
    logLevel: 'debug'
  });

  // Force re-render all mermaid diagrams
  window.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing Mermaid diagrams...');

    // Find all mermaid code blocks
    const mermaidBlocks = document.querySelectorAll('pre code.language-mermaid, pre code.mermaid, .mermaid');

    mermaidBlocks.forEach((block, index) => {
      // Create a div for the mermaid diagram
      const mermaidDiv = document.createElement('div');
      mermaidDiv.className = 'mermaid';
      mermaidDiv.setAttribute('data-processed', 'false');

      // Get the mermaid code
      let mermaidCode = block.textContent || block.innerText;

      // If it's in a code block, replace the pre/code with div
      if (block.tagName === 'CODE') {
        mermaidDiv.textContent = mermaidCode;
        const pre = block.closest('pre');
        if (pre) {
          pre.replaceWith(mermaidDiv);
        }
      } else {
        // Already a mermaid div
        block.setAttribute('data-processed', 'false');
      }
    });

    // Re-run mermaid
    try {
      mermaid.init(undefined, '.mermaid[data-processed="false"]');
      console.log('Mermaid diagrams initialized successfully');
    } catch (error) {
      console.error('Mermaid initialization error:', error);
    }
  });
} else {
  console.warn('Mermaid library not loaded');
}
