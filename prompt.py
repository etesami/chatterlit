PROMPT_INTERACTIVE = """ When responding and need more information, wait for user response and based on user response proceed with the next step."""

PROMPT_CODE_BLOCK = """ When responding with code, always use markdown code blocks with the appropriate language tag."""

PROMPT_JOBS = """ Adjust only the job title in the beginning paragraph to better fit the job description provided. Adjust only the positions title for the Work Experience section to better fit the job description provided. Keep the style and other details the same. Do not add new qualifications or experiences. If and only if the qualification is already stated but the job description emphasizes it more, you may rephrase it to better fit the job description. The priority is to keep the resume as close to the original as possible while making sure the job title and experience titles align with the job description."""

PROMPT_IMAGE = """
Create a high-quality, professional horizontal infographic with a 16:9 aspect ratio.
Design must remain fully inside the canvas at all times.
No text, icons, shapes, or graphics may touch or exceed the canvas edges.
Canvas & spacing rules:
• Apply generous inner padding on all sides (at least 5–8% of canvas width)
• Keep all text blocks within a safe margin
• Limit line length and font size so all text fits comfortably without wrapping off-canvas
• Avoid dense text areas; favor spacing over filling space
Layout & structure:
• Single-slide composition only (not a poster or document)
• One full-width title at the top, short and concise
• Main content arranged in 2–4 horizontal columns or bands
• Each section must fit entirely within its column or band
• Use clear spacing, dividers, or subtle background blocks to separate sections
• Avoid vertical stacking beyond one screen height
Text constraints:
• Headings: short, single-line when possible
• Bullet points: max 5–7 words per line
• No paragraphs or long sentences
• Prefer labels, keywords, and icons over text blocks
• Never use em dash
Visual style:
• Clean sans-serif typography
• Muted palette (soft blues, grays, neutrals with subtle accents)
• Use icons, arrows, diagrams, timelines, or flows to replace text wherever possible
• Maintain strong visual hierarchy and balanced horizontal composition
Content handling:
• Distill content into essential points only
• Highlight relationships, comparisons, processes, and hierarchies visually
• Ensure clarity, accuracy, and fast comprehension
Hard rule:
Nothing may overflow, clip, or extend beyond the horizontal or vertical canvas boundaries.
Use the following content as the source for the infographic: 
"""

PROMPTS = {
  "interactive": PROMPT_INTERACTIVE,
  "code_block": PROMPT_CODE_BLOCK,
  "jobs": PROMPT_JOBS,
  "image": PROMPT_IMAGE
}