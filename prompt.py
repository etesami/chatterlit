PROMPT_INTERACTIVE = """ When responding and need more information, wait for user response and based on user response proceed with the next step."""

PROMPT_CODE_BLOCK = """ When responding with code, always use markdown code blocks with the appropriate language tag."""

PROMPT_JOBS = """ Adjust only the job title in the beginning paragraph to better fit the job description provided. Adjust only the positions title for the Work Experience section to better fit the job description provided. Keep the style and other details the same. Do not add new qualifications or experiences. If and only if the qualification is already stated but the job description emphasizes it more, you may rephrase it to better fit the job description. The priority is to keep the resume as close to the original as possible while making sure the job title and experience titles align with the job description."""

PROMPT_IMAGE = """
Create a single-slide horizontal infographic with a strict 16:9 aspect ratio (1920x1080). The output must be landscape. Do not generate a square, vertical, cropped, or zoomed image.

ABSOLUTE CANVAS RULE (NON-NEGOTIABLE):
If the image would not be clearly horizontal (16:9), do not generate it.

CANVAS GEOMETRY — HARD CONSTRAINT:
The canvas is divided into two zones.

OUTER BLEED ZONE (FORBIDDEN AREA):
12% margin on the left, 12% on the right, 10% on the top, and 10% on the bottom. This outer area must remain completely empty background. No text, no icons, no shapes, no lines, no arrows, no shadows, no decorations of any kind may appear in this zone.

INNER SAFE AREA (ONLY ALLOWED CONTENT ZONE):
All content must be placed entirely inside the inner safe area. Treat the safe area as a strict, invisible bounding box.

Maintain a minimum clearance of at least 100 pixels from all canvas edges at all times. No element may touch, cross, clip, or visually press against the safe area boundary.

HARD FAILURE CONDITIONS:
Cropped or truncated text is not allowed.
Clipped icons or shapes are not allowed.
Text touching margins is not allowed.
If any of these occur, the image is invalid.

If there is any risk of overflow, you must reduce font size, shorten text, remove bullets, or simplify the layout. Fitting safely inside the safe area is more important than completeness.

MANDATORY PRE-FLIGHT FIT CHECK:
Before finalizing the image, verify that:
Every text block fits fully inside its container.
No text line runs outside its container.
No element crosses the safe area boundary.
Leftmost and rightmost content blocks have visible empty space beyond them.
If there is any uncertainty, reduce content density and font size.

LAYOUT RULES (STRICT):
Single slide only, not a poster or document.
Horizontal composition.
Title bar at the top inside the safe area, one line only.
Main content arranged in 2 to 4 horizontal columns or horizontal bands.
Each section must be contained within a subtle background block with internal padding.
Use generous spacing and dividers.
Avoid dense or edge-aligned layouts.

TYPOGRAPHY RULES:
Use a clean sans-serif font such as Inter or Helvetica.
Headings must be short and preferably single-line.
Bullets are limited to a maximum of 4 per section.
Each bullet must be 4 to 6 words maximum.
No paragraphs.
If content does not fit, remove bullets instead of shrinking margins.

VISUAL STYLE:
Professional and clean.
Muted palette using soft blues, grays, neutrals, and subtle accents.
Strong horizontal balance.
Prefer icons, diagrams, arrows, flows, and visual relationships over text.
Whitespace is intentional and desirable.

CONTENT PRIORITY:
Distill the source content to essentials.
Show relationships visually.
Leave empty space if needed.
Never risk clipping or truncation.

FINAL HARD RULE:
Nothing may overflow, clip, or touch the edges of the canvas. All elements must remain fully inside the safe area with generous whitespace.

Use the following content as the source for the infographic:

"""

PROMPTS = {
  "interactive": PROMPT_INTERACTIVE,
  "code_block": PROMPT_CODE_BLOCK,
  "jobs": PROMPT_JOBS,
  "image": PROMPT_IMAGE
}