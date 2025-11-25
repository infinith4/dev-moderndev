#!/usr/bin/env node

/**
 * Custom Markdown to PDF converter with Mermaid support
 * Uses Puppeteer for rendering
 */

const fs = require('fs').promises;
const path = require('path');
const { marked } = require('marked');
const puppeteer = require('puppeteer');

// HTML template for rendering
const htmlTemplate = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{title}}</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.0/github-markdown.min.css">
  <style>
    body {
      font-family: 'Noto Sans CJK JP', 'Noto Sans JP', 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
      padding: 2em;
      background: white;
    }
    .markdown-body {
      box-sizing: border-box;
      min-width: 200px;
      max-width: 980px;
      margin: 0 auto;
    }
    .mermaid {
      background-color: white;
      text-align: center;
      margin: 1em 0;
    }
  </style>
</head>
<body class="markdown-body">
{{content}}
</body>
</html>`;

async function convertMarkdownToPDF(inputFile, outputFile) {
  try {
    console.log(`Converting ${inputFile} to PDF...`);

    // Read markdown file
    const markdown = await fs.readFile(inputFile, 'utf-8');

    // Configure marked to handle mermaid code blocks
    const renderer = new marked.Renderer();
    const originalCodeRenderer = renderer.code.bind(renderer);

    renderer.code = function(code, language) {
      if (language === 'mermaid') {
        // Return mermaid div instead of code block
        return `<div class="mermaid">${code}</div>`;
      }
      return originalCodeRenderer(code, language);
    };

    marked.setOptions({
      renderer: renderer,
      gfm: true,
      breaks: false,
      headerIds: false
    });

    // Convert markdown to HTML
    const contentHtml = marked(markdown);

    // Get title from first heading or filename
    const titleMatch = markdown.match(/^#\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1] : path.basename(inputFile, '.md');

    // Generate final HTML
    const html = htmlTemplate
      .replace('{{title}}', title)
      .replace('{{content}}', contentHtml);

    // Launch Puppeteer
    const browser = await puppeteer.launch({
      headless: 'new',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-web-security'
      ]
    });

    const page = await browser.newPage();

    // Set content
    await page.setContent(html, {
      waitUntil: 'networkidle0'
    });

    // Add Mermaid library
    await page.addScriptTag({
      url: 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js'
    });

    // Initialize and render Mermaid diagrams
    await page.evaluate(async () => {
      mermaid.initialize({
        startOnLoad: false,
        theme: 'default',
        securityLevel: 'loose',
        fontFamily: 'Noto Sans CJK JP, sans-serif'
      });

      const mermaidDivs = document.querySelectorAll('.mermaid');
      if (mermaidDivs.length > 0) {
        await mermaid.run({
          querySelector: '.mermaid'
        });
        console.log(`Rendered ${mermaidDivs.length} Mermaid diagrams`);
      }
    });

    // Wait a bit for diagrams to fully render
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Generate PDF
    await page.pdf({
      path: outputFile,
      format: 'A4',
      margin: {
        top: '10mm',
        right: '10mm',
        bottom: '10mm',
        left: '10mm'
      },
      printBackground: true
    });

    await browser.close();

    console.log(`✓ Successfully converted ${inputFile} to ${outputFile}`);
    return true;
  } catch (error) {
    console.error(`✗ Error converting ${inputFile}:`, error.message);
    return false;
  }
}

// Main function
async function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error('Usage: node markdown-to-pdf.js <input.md> <output.pdf>');
    process.exit(1);
  }

  const [inputFile, outputFile] = args;

  // Ensure output directory exists
  const outputDir = path.dirname(outputFile);
  await fs.mkdir(outputDir, { recursive: true });

  // Convert
  const success = await convertMarkdownToPDF(inputFile, outputFile);

  process.exit(success ? 0 : 1);
}

// Run if called directly
if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { convertMarkdownToPDF };
