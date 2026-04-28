"""300+ Prompt Templates Library — Photography, Design, UI/UX, Branding, Illustration, Animation, Print, 3D"""

# Difficulty levels per category: "beginner" | "professional" | "expert"
# Use get_category_prompts(category, level) to filter by difficulty.

PROMPTS = {
    # CATEGORY A: GENERAL PHOTOGRAPHY
    "general_photography": [
        "Ultra HD portrait photography of a young Indian professional, wearing traditional kurta with modern styling, soft natural lighting, bokeh background, professional headshot, 8k quality, shot on Canon 5D",
        "Candid lifestyle photography of Indian family having chai on rooftop, golden hour lighting, warm tones, authentic moments, shot on Fujifilm, 8k quality, shallow depth of field",
        "Street photography of Indian marketplace, vibrant colors, traditional vendors, authentic culture, natural lighting, 8k quality, shot on Leica, documentary style",
        "Fashion photography of Indian woman wearing designer saree, traditional jewelry, studio lighting, professional model shot, 8k quality, high fashion magazine style",
        "Travel photography of Indian temple architecture, ancient stone work, dramatic lighting, golden hour, 8k quality, architectural photography, wide angle lens",
    ],
    
    # CATEGORY B: WOMEN'S PHOTOSHOOT
    "women_professional": [
        "Professional Indian woman in modern office wear, confidence, natural lighting, studio background, corporate aesthetic, 8k quality, shot on Canon EOS",
        "Indian woman in traditional saree, elegant pose, studio lighting, neutral background, professional jewelry, glamour photography, 8k quality",
        "Young Indian woman in casual modern outfit, natural outdoor lighting, park/garden background, lifestyle photography, approachable vibe, 8k quality",
        "Indian woman in fusion wear (saree + leather jacket), edgy modern aesthetic, urban background, fashion editorial style, 8k quality",
        "Indian woman in traditional bridal wear, heavy jewelry, dramatic lighting, regal pose, wedding photography style, 8k quality",
        "Indian woman in swimwear/beach outfit, tropical background, golden hour lighting, lifestyle photography, confident pose, 8k quality",
        "Young Indian woman in gym/fitness wear, active pose, motivational lighting, athletic aesthetic, 8k quality",
        "Indian woman in ethnic wear (anarkali suit, lehenga), traditional jewelry, festive lighting, celebration mood, 8k quality",
    ],
    
    "women_transform": [
        "Professional Indian woman in formal corporate office wear. Preserve recognizable facial features from reference image. Pose: standing tall with shoulders back, one hand on desk, head slightly tilted upward showing confidence. Setting: office environment with studio lighting. Expressions: confident, professional eye contact. Output: 8k quality, professional headshot aesthetic.",
        
        "Indian woman in traditional silk saree. Preserve facial characteristics from reference image. Pose: standing gracefully with one shoulder forward, hand on chest, three-quarters body angle. Expressions: soft, serene, sophisticated. Lighting: studio lighting, glamour photography style. Output: 8k quality, elegant aesthetic.",
        
        "Young Indian woman in modern fusion wear (traditional meets contemporary). Preserve facial features from reference image. Pose: dynamic power pose, one leg forward, confident stance. Setting: professional lighting, editorial fashion aesthetic. Expressions: confident, modern. Output: 8k quality, high-fashion magazine style.",
        
        "Indian bride in traditional bridal wear (ornate lehenga/saree). Preserve facial features from reference image. Pose: regal posture, one hand raised showing jewelry, seated or standing. Setting: dramatic warm lighting. Expressions: dignified, radiant. Output: 8k quality, wedding photography aesthetic.",
        
        "Indian woman as lifestyle influencer. Preserve facial characteristics from reference image. Pose: candid walking pose with natural arm movement, relaxed confident stride, turning toward camera. Setting: natural lighting. Expressions: engaging smile, Instagram-worthy body language. Output: 8k quality, contemporary lifestyle.",
        
        "Glamorous Indian woman with theatrical makeup. Preserve facial features from reference image. Pose: sitting or reclined in magazine cover pose, one arm extended gracefully. Setting: professional beauty lighting, dramatic glamorous setting. Expressions: confident, luxurious aesthetic. Output: 8k quality, luxury photography.",
        
        "Fit Indian woman in gym/fitness wear. Preserve facial features from reference image. Pose: dynamic athletic pose, one leg extended or lunging, arms flexed. Setting: motivational lighting, fitness environment. Expressions: powerful, energetic. Output: 8k quality, fitness model aesthetic.",
        
        "Indian woman in traditional wedding ceremony ethnic wear. Preserve facial characteristics from reference image. Pose: standing with hands in traditional position, celebratory posture. Setting: festive ceremonial lighting. Expressions: joyful, radiant smile. Output: 8k quality, traditional celebration.",
        
        "Glamorous Indian woman as Bollywood celebrity. Preserve facial features from reference image. Pose: dramatic pose leaning against surface, one leg bent, theatrical hand placement. Setting: dramatic red carpet lighting. Expressions: expressive, confident posture. Output: 8k quality, cinema-quality photography.",
        
        "Indian woman as travel influencer. Preserve facial features from reference image. Pose: adventurous action pose (standing on cliff, hiking stance), looking toward horizon. Setting: exotic destination background. Expressions: adventurous body language. Output: 8k quality, wanderlust aesthetic.",
    ],
    
    # CATEGORY C: MEN'S PHOTOSHOOT
    "men_professional": [
        "Professional Indian man in formal business suit, confident pose, office environment, corporate photography, 8k quality, shot on Canon 5D Mark IV",
        "Young Indian man in traditional ethnic wear (kurta pajama), studio lighting, traditional aesthetic, cultural photography, 8k quality",
        "Indian man in casual smart wear (shirt + jeans), outdoor lighting, natural background, lifestyle photography, approachable vibe, 8k quality",
        "Fit Indian man in gym wear/fitness clothing, athletic pose, gym environment or outdoor, fitness photography, motivational aesthetic, 8k quality",
        "Indian man in traditional festival wear (dhoti, sherwani), golden lighting, celebration mood, traditional photography, 8k quality",
        "Young Indian man in streetwear/urban fashion, trendy modern outfit, urban background, fashionable aesthetic, 8k quality",
        "Indian man in semi-formal Indian ethnic wear (Nehru jacket with traditional elements), sophisticated pose, studio lighting, elegant aesthetic, 8k quality",
        "Indian man in traditional South Indian wear (veshti, traditional top), cultural photography, temple background, authentic traditional style, 8k quality",
    ],
    
    "men_transform": [
        "Professional Indian man in formal business suit. Preserve recognizable facial features from reference image. Pose: standing tall with hands in power position, slight body angle showing confidence. Setting: office background with corporate lighting. Expressions: direct eye contact, commanding executive presence. Output: 8k quality, professional headshot aesthetic.",
        
        "Handsome Indian man in traditional kurta pajama. Preserve facial characteristics from reference image. Pose: standing gracefully with one hand on chest, dignified posture. Setting: studio lighting, elegant background. Expressions: soft, focused gaze, sophisticated. Output: 8k quality, cultural photography aesthetic.",
        
        "Athletic Indian man in gym wear. Preserve facial features from reference image. Pose: dynamic power pose with arms flexed, strong confident stance. Setting: fitness environment with motivational lighting. Expressions: powerful, energetic. Output: 8k quality, fitness model aesthetic.",
        
        "Glamorous Indian man as Bollywood actor. Preserve facial features from reference image. Pose: dramatic pose leaning against surface, one hand raised. Setting: dramatic red carpet lighting, theatrical environment. Expressions: intense eye contact, confident posture. Output: 8k quality, cinema-quality photography.",
        
        "Trendy Indian man as lifestyle influencer. Preserve facial characteristics from reference image. Pose: relaxed confident standing pose, one hand in pocket. Setting: natural lighting. Expressions: engaging smile toward camera, Instagram aesthetic. Output: 8k quality, contemporary lifestyle.",
        
        "Indian man in traditional festival wear (sherwani, ethnic). Preserve facial features from reference image. Pose: standing regal with hands gracefully placed. Setting: golden warm lighting. Expressions: celebratory, proud, warm. Output: 8k quality, festive aesthetic.",
        
        "Indian man as travel influencer. Preserve facial features from reference image. Pose: adventurous action pose (standing on mountain, exploring), looking toward horizon. Setting: exotic location background. Expressions: adventurous body language, wanderlust vibe. Output: 8k quality, adventure aesthetic.",
        
        "Artistic creative Indian man. Preserve facial characteristics from reference image. Pose: sophisticated pose leaning or seated artistically. Setting: artistic background, creative environment. Expressions: thoughtful, composed, cultured aesthetic. Output: 8k quality, creative professional.",
        
        "Luxury lifestyle Indian man. Preserve facial features from reference image. Pose: standing confidently in premium designer wear. Setting: high-end upscale background. Expressions: sophisticated, composed, elegant posture. Output: 8k quality, luxury aesthetic.",
        
        "Charismatic Indian man for dating profile. Preserve facial features from reference image. Pose: relaxed approachable pose with gentle smile. Setting: warm romantic lighting. Expressions: welcoming, engaging direct eye contact. Output: 8k quality, approachable romantic aesthetic.",
    ],
    
    # CATEGORY D: COUPLES
    "couples_general": [
        "Indian couple pre-wedding photoshoot, romantic pose, outdoor garden setting, golden hour lighting, traditional jewelry, professional photography, 8k quality, shot on Canon 5D",
        "Indian couple in traditional wedding wear (bride in lehenga, groom in sherwani), ornate jewelry, festive lighting, wedding photography style, regal aesthetic, 8k quality",
        "Young Indian couple in casual modern outfit, candid romantic moment, outdoor park setting, natural lighting, lifestyle photography, authentic vibe, 8k quality",
        "Indian couple in ethnic fusion wear, modern styling with traditional elements, studio lighting, contemporary photography, 8k quality",
        "Couple in traditional festival outfit (Holi colors, celebration mood), playful energetic pose, festive lighting, joyful atmosphere, 8k quality",
        "Indian couple in formal ethnic wear (woman in saree, man in formal kurta), elegant pose, studio lighting, sophisticated aesthetic, 8k quality",
        "Young couple in beach/casual wear, romantic coastal setting, sunset lighting, vacation mood, lifestyle photography, intimate moment, 8k quality",
        "Couple during Indian wedding ceremony, bride in bridal saree, groom in traditional sherwani, temple setting, ceremonial photography, 8k quality",
    ],
    
    "couples_transform": [
        "Couple portrait transformation using two reference images. Preserve both individuals' recognizable facial features (face shape, eyes, nose, lips, skin tone) while keeping natural likeness. Couple standing close, slightly leaning toward each other. Hands: fingers intertwined, her right hand on his shoulder, his right hand gently holding hers. Head angle: soft tilt toward each other (~45°). Expressions: warm, subtle smiles. Style: 90s vintage fashion shoot. Outfits: pastel tones, soft textures, minimal patterns. Lighting: warm softbox with golden-hour glow. Background: blurred vintage cityscape or soft gradient. Camera: slightly above eye level, shallow depth of field. Output: high-resolution, cinematic, soft romantic aesthetic.",
        
        "Indian couple pre-wedding photoshoot. Preserve facial features from both reference images. Pose: bride facing forward, groom standing behind with arms around bride, both turning toward camera. Setting: outdoor garden with golden hour lighting. Traditional jewelry and elegant aesthetic. Expressions: warm, romantic connection. Lighting: softbox with golden hour glow. Camera: shallow depth of field emphasizing couple connection. Output: 8k quality, professional photography, romantic and intimate mood.",
        
        "Indian wedding couple portrait. Preserve recognizable facial features for both subjects from reference images. Pose: bride and groom facing each other, joyful expressions, gentle body connection. Bride in bridal saree/lehenga, groom in traditional sherwani. Setting: temple or ceremonial backdrop. Lighting: warm, golden ceremonial lighting. Camera: centered composition, slight elevated angle. Output: high-resolution, wedding photography aesthetic, celebratory mood.",
        
        "Engaged Indian couple sitting close together. Preserve facial characteristics from both reference images. Pose: couple seated, hands intertwined, facing camera. Setting: studio environment with neutral background. Lighting: professional studio setup, soft directional light. Expressions: romantic, intimate connection. Outfits: formal elegant wear. Output: 8k quality, professional engagement photography, intimate moment.",
        
        "Indian couple celebrating anniversary. Preserve facial features from both reference images. Pose: standing facing each other with warm embrace. Setting: romantic dining environment with candlelight ambiance. Outfits: formal elegant wear. Expressions: joyful, celebratory connection. Lighting: warm candlelight with subtle key light. Camera: intimate framing. Output: high-resolution, romantic atmosphere, celebratory aesthetic.",
        
        "Couple on honeymoon vacation. Preserve facial features from both reference images. Pose: walking hand in hand toward horizon. Setting: exotic tropical background, sunset. Outfits: casual vacation wear. Expressions: relaxed, joyful. Lighting: golden-hour sunset glow. Camera: full-body composition with landscape. Output: high-resolution, wanderlust aesthetic, adventure mood.",
        
        "Indian couple celebrating Holi festival. Preserve facial characteristics from both reference images. Pose: playfully posing together with colored powder in air. Setting: outdoor festive environment. Outfits: colorful traditional festival clothes. Expressions: energetic, joyful, playful. Lighting: bright festive lighting, colorful powder dust. Camera: dynamic action shot. Output: high-resolution, celebration mood, vibrant energetic aesthetic.",
        
        "Couple on romantic dinner date. Preserve facial features from both reference images. Pose: seated at table, leaning toward each other, intimate eye contact. Setting: elegant restaurant with candlelight. Outfits: formal elegant wear. Expressions: warm, loving, connected. Lighting: candlelight with warm accent lighting. Camera: intimate medium shot. Output: high-resolution, intimate romantic aesthetic.",
        
        "Modern Indian couple as influencers. Preserve facial characteristics from both reference images. Pose: back-to-back, both looking toward camera with confident relaxed expressions. Setting: Instagram-worthy contemporary background. Outfits: contemporary stylish wear. Lighting: natural or bright studio lighting. Camera: full-body composition. Output: high-resolution, modern aesthetic, relatable and stylish mood.",
        
        "Luxury lifestyle Indian couple. Preserve facial features from both reference images. Pose: standing together facing forward, confident elegant posture. Setting: high-end upscale background. Outfits: premium designer wear. Lighting: sophisticated professional lighting. Camera: full-body composition with refined framing. Output: high-resolution, sophisticated upscale aesthetic.",
    ],
    
    # CATEGORY F: DESIGN & POSTERS
    "design_posters": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Motivational Instagram post, bold white text on dark gradient background, simple geometric shapes, clean modern layout, 1080x1080px"},
        {"level": "beginner", "prompt": "Diwali festival graphic, gold and red colours, diya illustration, centered text, festive mood, Instagram square format 1080x1080"},
        {"level": "beginner", "prompt": "Fitness quote poster, dark gym background, bright accent text, simple icon, bold sans-serif font, Instagram story 1080x1920"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Minimalist motivational poster, bold typography, Indian cultural geometric patterns inspired by Rangoli, split-tone color palette (deep navy + saffron), modern flat design, grid-based composition, 1920x1080, 300dpi print-ready"},
        {"level": "professional", "prompt": "Vibrant social media graphic, Holi festival theme, dynamic color splash (magenta, cyan, yellow), editorial-style photo overlay, modern sans-serif headline, rule-of-thirds layout, 1080x1350 Instagram portrait"},
        {"level": "professional", "prompt": "Women empowerment poster, strong silhouette of Indian woman, duotone purple/gold colour scheme, editorial typography hierarchy, negative space composition, 1080x1350, Instagram-optimised"},
        {"level": "professional", "prompt": "Travel destination carousel slide, golden-hour photography of Indian landmark, magazine-style layout, white space, elegant serif headline + body copy, Instagram carousel 1080x1080"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Avant-garde conceptual poster, surreal photomontage blending Mughal architecture with cyberpunk neon aesthetics, Glitch art texture overlay, chromatic aberration, brutalist grid, custom variable font headline, 4K 3840x2160, bleed-safe print"},
        {"level": "expert", "prompt": "Luxury brand announcement poster, ultra-minimal layout, single hero product floating on marble texture, gold foil emboss simulation, Swiss typography system (Helvetica Neue), precise kerning, 5pt grid, A2 print 420x594mm 300dpi CMYK"},
        {"level": "expert", "prompt": "Data-driven infographic poster, premium financial dashboard aesthetic, dark glass-morphism panels, neon accent data visualisations, custom icon set, hierarchical typographic scale, 1920x1080 UHD web + print dual output"},
    ],

    # CATEGORY G: REEL SCRIPTS
    "reel_scripts": [
        {"level": "beginner", "prompt": "15-second Reel: morning routine, warm lighting, soft background music, 3 simple cuts, text overlay with steps"},
        {"level": "beginner", "prompt": "30-second Reel: before/after transformation, split-screen effect, trending audio, motivational text overlay"},
        {"level": "beginner", "prompt": "15-second POV Reel: relatable everyday Indian life moment, single location, trending sound, one text caption"},
        {"level": "professional", "prompt": "30-second educational Reel: 'Did You Know' Indian history fact, kinetic text overlays, quick 4-cut edit, royalty-free upbeat audio, hook in first 2 seconds, end-screen CTA"},
        {"level": "professional", "prompt": "45-second Day-in-life Reel: Indian entrepreneur morning routine, 6-cut sequence, golden-hour aesthetic, voiceover narration, lower-third labels, engagement CTA at end"},
        {"level": "professional", "prompt": "30-second product showcase Reel: product reveal with dramatic lighting reveal, slow-motion detail shots, trending audio sync, logo sting at end, vertical 9:16 format"},
        {"level": "expert", "prompt": "60-second cinematic brand story Reel: 4K footage, colour graded in warm film emulation LUT, seamless jump-cut rhythm synced to bass drops, motion-tracked typography, dynamic aspect-ratio transitions (16:9→9:16), brand-colour grade, professional colour science"},
        {"level": "expert", "prompt": "45-second viral challenge Reel: original Indian cultural twist on global trend, multi-location shoot, drone intro shot, match-cut transitions, waveform-synced text animation, platform-native interactive sticker CTA"},
    ],

    # CATEGORY H: CAPTIONS
    "captions_templates": [
        {"level": "beginner", "prompt": "POV: That one chai shop uncle who remembers your entire family history 😂☕ #IndianLife #ChaiLife #Relatable"},
        {"level": "beginner", "prompt": "Morning motivation: small steps lead to big changes 💪 #MondayMotivation #GrowthMindset #Fitness"},
        {"level": "professional", "prompt": "Your 2026 glow-up starts now. Here's what 5 Indian creators did to transform their life 💫 #GoalSetting #IndianEntrepreneurs"},
        {"level": "professional", "prompt": "She learned this from her grandmother. Now she earns 6 figures from it. Here's her story 🧵 #IndianWomen #TraditionMeetsModern"},
        {"level": "professional", "prompt": "[Achievement unlocked]. But the real win? Still having chai with my mom every Sunday ☕❤️ #Grateful #MilestoneReached"},
        {"level": "expert", "prompt": "Real talk: [honest struggle statement]. Not everything is Instagram perfect—but here's exactly how I'm building through it 💪 Thread 🧵 #RealTalk #Authentic #GrowthJourney #CreatorEconomy"},
        {"level": "expert", "prompt": "I studied 50 viral Indian creator accounts. The one thing they all do differently? [insight] — full breakdown below 👇 Save this. #ContentStrategy #ViralGrowth #IndianCreators"},
    ],

    # CATEGORY I: EMAIL SUBJECTS
    "email_subjects": [
        {"level": "beginner", "prompt": "Your weekly Instagram tips are here 📱"},
        {"level": "beginner", "prompt": "3 quick wins for your content this week 🚀"},
        {"level": "professional", "prompt": "Indian Secret Productivity Hack (Borrowed from Ancient Texts) 📜"},
        {"level": "professional", "prompt": "How 15K Indian Creators Made $X This Year (Without Selling)"},
        {"level": "professional", "prompt": "[First Name], Your Personalised Growth Plan Is Ready"},
        {"level": "expert", "prompt": "The algorithm-proof content framework top 1% Indian creators use (never shared publicly)"},
        {"level": "expert", "prompt": "Why your reach dropped 40% last month — and the exact fix 3 creators used to bounce back"},
    ],

    # ─── NEW CATEGORY 1: UI/UX DESIGN ─────────────────────────────────────────
    "ui_ux_design": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Clean mobile app login screen, white background, blue primary button, email and password fields, simple logo at top, iOS style, Figma mockup"},
        {"level": "beginner", "prompt": "Simple dashboard UI, card-based layout, 4 stat tiles, light grey background, clean sans-serif font, mobile-first design"},
        {"level": "beginner", "prompt": "E-commerce product page, product image left, details right, big 'Add to Cart' button, minimal design, responsive layout"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Fitness tracking iOS app — onboarding screen 3/5: animated progress ring in saffron/teal accent, dark background, SF Pro Display typography, bottom sheet micro-interaction, safe-area-aware layout, WCAG AA contrast, 390x844px @3x export"},
        {"level": "professional", "prompt": "SaaS analytics dashboard, glass-morphism sidebar, gradient area charts, data table with sortable columns, dark mode, Inter typeface, 8pt spacing grid, 1440px desktop breakpoint, Figma auto-layout components"},
        {"level": "professional", "prompt": "Food delivery app home screen, card-based restaurant grid, sticky search bar, category pill filters, skeleton loading state, Material You colour scheme, 360x800 Android, 4dp corner radius system"},
        {"level": "professional", "prompt": "FinTech wallet app — transaction history screen, timeline list with category icons, income/expense colour split (green/red), mini sparkline per entry, bottom nav bar, iOS Human Interface Guidelines compliant, SF Symbols icons"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "AI-powered productivity app — command palette overlay, frosted glass blur (backdrop-filter 20px), animated type-ahead suggestions with confidence scores, keyboard shortcut badges, tokenised design system variables, dark/light theme adaptive, WCAG AAA, Figma variables + modes"},
        {"level": "expert", "prompt": "Luxury real-estate web app — immersive full-bleed 3D property viewer, spatial UI floating controls, cinematic parallax scroll, editorial serif + geometric sans type pairing, 12-column 1920px grid, micro-animation system (Lottie + Framer Motion), design token documentation"},
        {"level": "expert", "prompt": "B2B enterprise data platform — complex nested table with inline editing, multi-select bulk actions, contextual command bar, resizable column system, drag-to-reorder rows, advanced filter builder (AND/OR logic), accessibility: screen-reader ARIA live regions, focus trap management, Storybook component docs"},
    ],

    # ─── NEW CATEGORY 2: BRAND IDENTITY ───────────────────────────────────────
    "brand_identity": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Simple logo design for Indian food brand, round badge style, warm orange and brown colours, fork and leaf icon, clean sans-serif name"},
        {"level": "beginner", "prompt": "Basic brand colour palette for wellness brand, 5 swatches, earthy greens and creams, hex codes labelled, Canva-style presentation"},
        {"level": "beginner", "prompt": "Social media profile kit, matching profile picture + banner for Instagram, consistent colours and fonts, minimal aesthetic"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Premium ayurvedic wellness brand identity: wordmark in elegant serif (Garamond variant), lotus motif monogram, brand palette (ivory, forest green, burnished gold), primary + secondary logo lockups, minimum size rules, clear-space guidelines, A4 brand sheet"},
        {"level": "professional", "prompt": "D2C Indian fashion brand — full visual identity: geometric batik-inspired pattern system, brand typeface pairing (display + body), 6-colour palette with usage ratios, logo on light/dark/pattern backgrounds, packaging mockup (garment tag + shopping bag), brand guidelines PDF"},
        {"level": "professional", "prompt": "Tech startup brand kit: bold geometric wordmark, icon system (6 custom SVG icons), primary blue-violet palette + neutrals, Inter + Space Grotesk type system, business card + letterhead + email signature mockups, Figma brand token library"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Heritage luxury jewellery brand identity overhaul: custom variable serif wordmark with optical weight compensation, micro-pattern inspired by historic Bidriware metalwork, 3-tier colour system (hero / supporting / accent), holographic foil simulation for print, adaptive logo for AR contexts, comprehensive 60-page brand book with do/don't examples"},
        {"level": "expert", "prompt": "Global fintech brand system: responsive logo family (full / compact / icon / favicon), internationalisation-ready typeface (Latin + Devanagari + Arabic), semantic colour token architecture (global → alias → component), motion identity guidelines (easing curves, timing functions), accessibility audit for all brand applications, Figma Tokens JSON export"},
    ],

    # ─── NEW CATEGORY 3: ILLUSTRATION & DIGITAL ART ───────────────────────────
    "illustration_art": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Cute flat illustration of Indian street food cart, bright colours, simple shapes, no shadows, vector style, white background"},
        {"level": "beginner", "prompt": "Simple character illustration of Indian woman in saree, bold outline, flat colour fill, kawaii proportions, digital art"},
        {"level": "beginner", "prompt": "Minimal line art of Indian city skyline, single colour, thin strokes, landmarks silhouetted, suitable for t-shirt print"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Editorial illustration — Indian woman coder. Style: holographic UI elements floating around, isometric perspective. Palette: vibrant jewel tones. Technique: Procreate digital painting with textured grain. Output: 2400x1600px editorial format."},
        {"level": "professional", "prompt": "Children's book illustration — Indian village festival at night. Focus: Diwali lamps reflected in river. Style: warm painterly gouache, soft lighting. Composition: rich storytelling. Output: 3000x2000px, 300dpi."},
        {"level": "professional", "prompt": "Concept art — Indian mythology character (Arjuna as modern archer hero). Pose: dynamic action, detailed Mahabharata-inspired armour. Lighting: dramatic rim-light. Technique: painterly rendering. Composition: cinematic. Output: 2K square format."},
        {"level": "professional", "prompt": "Infographic illustration — Indian spice market. 8 spice icons with hand-drawn linework, watercolour texture. Labels: editorial serif fonts. Palette: warm earthy tones. Layout: A3 print format."},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Surrealist digital painting — Indian classical dancer transforming into cosmic deity. Subject: body formed from micro-marigolds. Palette: terracotta → celestial indigo. Technique: individual petal rendering at Beeple-level detail. Output: 8K UHD."},
        {"level": "expert", "prompt": "Graphic novel cover — dystopian Mumbai 2087. Palette: acid yellow / noir black / rust orange. Technique: ink-wash + digital hybrid with layered atmospheric haze. Composition: cyberpunk Indian characters (foreground) → broken architecture (mid-ground) → blood-red sky. Format: 210x297mm A4 bleed. Influence: Frank Miller."},
        {"level": "expert", "prompt": "Generative mandala — algorithmically composed from Tamil Kolam patterns. Structure: parametric symmetry. Palette: 256-colour gradient HSL spectrum. Detail: ultra-fine linework at 0.1pt. Output: large-format canvas 120x120cm at 300dpi."},
    ],

    # ─── NEW CATEGORY 4: ANIMATION & MOTION GRAPHICS ─────────────────────────
    "animation_motion": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Simple logo reveal animation, fade-in with slight scale, 2 seconds, clean white background, ease-in-out timing, exported as GIF and MP4"},
        {"level": "beginner", "prompt": "Instagram story animated text, bold headline types on screen word by word, colourful background, 5 seconds loop, After Effects template style"},
        {"level": "beginner", "prompt": "Basic loading spinner animation, circular progress ring in brand colour, smooth 1-second loop, transparent background, Lottie JSON format"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Brand intro sting (3-sec). Wordmark assembled by particle swarm. Background: deep blue. Lighting: subtle lens flare. Audio: synced to logo hit beat. Tool: After Effects. Output: 1920x1080 ProRes."},
        {"level": "professional", "prompt": "Animated explainer (30-sec) — UPI payment flow. Style: flat 2D with smooth transitions, kinetic typography. Audio: royalty-free upbeat track. Context: Indian market. Output: 1080x1920 vertical + 1920x1080 horizontal."},
        {"level": "professional", "prompt": "Social media carousel animation. 5-slide product launch sequence. Motion: consistent language (slide-in left, scale pop). Palette: brand colours. Export: GIF + MP4 auto-advancing. Format: 1080x1080, 24fps."},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Cinematic title sequence — Indian web series. Technique: hand-drawn frame-by-frame. Content: mythological scenes → modern urban. Frame rate: 12fps artistic stagger. Texture: traditional miniature painting. Score: orchestral + electronic sync. Output: 4K 4096x2160, film grain, 45-sec."},
        {"level": "expert", "prompt": "Real-time 3D motion graphics — Rangoli powder spreading. Technique: GPU particle system with physics-based colour mixing. Shader: custom GLSL blend modes. Render: 60fps WebGL with mouse-tracking interactivity + 4K pre-rendered social version. Loopable."},
        {"level": "expert", "prompt": "Data visualisation animation — India population density choropleth (10-year time-lapse). Easing: custom per-state transitions. Camera: pan system across regions. Pipeline: d3.js + After Effects polish. Output: 1920x1080 broadcast-safe with synced lower-third annotations."},
    ],

    # ─── NEW CATEGORY 5: PHOTOGRAPHY STYLES ──────────────────────────────────
    "photography_styles": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Bright and airy portrait, Indian woman, natural window light, white background, soft shadows, clean Instagram aesthetic, shot on iPhone"},
        {"level": "beginner", "prompt": "Warm golden-hour street photo, Indian marketplace, orange tone, candid people, shot on smartphone, lifestyle feel"},
        {"level": "beginner", "prompt": "Flat lay product photo, Indian spices in small bowls, warm wood background, natural light, minimal props, overhead angle"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Noir portrait — 1950s Mumbai café setting. Subject: Indian man. Lighting: single overhead tungsten, deep shadow pools (70% black), wet-pavement reflections. Film: Kodak 5219 emulation, 800 ISO grain. Lens: 85mm f/1.4. Colour: desaturated mid-tones, punchy highlights."},
        {"level": "professional", "prompt": "Surreal fine-art portrait — Indian woman + Ajanta fresco merge. Concept: skin painted with intricate fresco patterns. Lighting: soft ethereal. Palette: teal-terracotta-gold. Technique: double-exposure composite. Depth: dreamlike DOF. Format: medium-format aesthetic 4:3 crop, 8K."},
        {"level": "professional", "prompt": "High-fashion editorial — Indian model in avant-garde silhouette. Setup: stark studio with large-format strobe (sharp octabox). Lighting: dramatic deep shadow. Composition: editorial negative space (Vogue India aesthetic). Sensor: Phase One 150MP. Format: 8x10 portrait."},
        {"level": "professional", "prompt": "Documentary street — blue-hour chai stall, Old Delhi. Lighting: available light (fluorescent + fire). Texture: authentic gritty. Lens: 35mm f/2.8 wide-angle. Composition: photojournalism style with intentional motion blur on vendor hands. Film: Tri-X 400 B&W conversion."},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Architectural study — 19th-century Indo-Saracenic railway station. Camera: 4x5 view camera with perspective correction. Exposure: zone system (Zone III-VIII). Print: platinum-palladium emulation. Detail: ultra-sharp corner-to-corner. Composition: architectural symmetry (Ansel Adams style). Output: 8K scan."},
        {"level": "expert", "prompt": "Multiple-exposure fine art — Indian classical dance (Bharatanatyam). Technique: 7-layer in-camera exposure with intentional colour-channel separation. Result: motion-spectrum rainbow body trail. Speed: 1/8000s per frame. Render: single raw file combined. Style: abstract-expressionist. Sensor: 100MP."},
        {"level": "expert", "prompt": "Computational macro — Indian coin collection. Technique: 200-image focus-stack at 1:1 macro. Step: 0.02mm interval. Processing: zerene stacker. Detail: infinitely sharp surfaces. Resolution: 500MP effective output. Quality: scientific illustration, museum-archive standard."},
    ],

    # ─── NEW CATEGORY 6: PRINT DESIGN ────────────────────────────────────────
    "print_design": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Simple A5 flyer for Indian restaurant, food photo centre, name at top, address at bottom, warm colours, easy to read, print-ready"},
        {"level": "beginner", "prompt": "Basic event poster for Navratri festival, large title text, date and venue, decorative border, saffron and red colours, A4 size"},
        {"level": "beginner", "prompt": "Simple business card, name and contact details, minimal design, white background, brand colour accent stripe, 90x55mm standard size"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Wedding invitation suite — laser-cut gate-fold card. Material: 400gsm deep burgundy paper. Typography: gold foil letterpress. Motifs: watercolour floral Indian patterns. Components: RSVP card + inner envelope. Size: 5x7 inch. Specs: 300dpi CMYK, 3mm bleed & crop marks."},
        {"level": "professional", "prompt": "Magazine cover — Indian fashion monthly. Layout: full-bleed editorial portrait + masthead (custom display type). Cover lines: hierarchy (kicker/headline/deck). Specs: A4 bleed 216x303mm, 300dpi, ISO Coated v2 profile. Placement: barcode + price (newsstand-optimised contrast)."},
        {"level": "professional", "prompt": "Corporate annual report spread — double-page layout. Content: infographic-led with elegant financial charts. Design: 12-column grid, brand type system, photography + illustration mix. Size: A4 landscape. Specs: 4mm bleed, Pantone spot colour, print-ready InDesign format."},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Museum exhibition catalogue — 128-page art book. Grid: Swiss system. Typography: Futura + Caslon. Layout: full-bleed artwork reproductions opposite scholarly text. Features: running heads, footnotes, index, bibliography. Binding: perfect-bound 230x280mm. Specs: ICC-profiled FOGRA51 pre-press, ISBN barcode."},
        {"level": "expert", "prompt": "Artisanal packaging system — premium Indian tea. Box: handmade paper with custom letterpress label. Details: heritage illustration, deboss lid pattern, tissue wrap with spot UV mark. Design: unboxing sequence. Features: eco material callouts, regulatory text hierarchy. Output: dieline for corrugated insert + production spec sheet."},
    ],

    # ─── NEW CATEGORY 7: 3D PRODUCT DESIGN ───────────────────────────────────
    "product_3d": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "3D product mockup of smartphone app on iPhone, clean studio background, soft shadows, one light source, realistic render, white backdrop"},
        {"level": "beginner", "prompt": "Simple 3D render of perfume bottle, glass material, white background, soft studio lighting, product photography look"},
        {"level": "beginner", "prompt": "3D food product visualisation, Indian snack box packaging, flat lay angle, warm lighting, realistic shadows, e-commerce style"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Hero product render — premium skincare serum bottle. Materials: borosilicate glass, gold metallic dropper cap. Lighting: 3-point studio rig with caustic refractions on marble surface. Render: 4K photorealistic PBR in Blender Cycles or Cinema 4D Octane. Ambient: white + soft warm."},
        {"level": "professional", "prompt": "Architectural product viz — Indian modular furniture in contemporary apartment. Materials: natural oak veneer, matte black metal. Lighting: HDRI morning light through floor-to-ceiling window, subsurface scatter on fabric. Effects: depth-of-field blur. Output: 4K interior render, ArchViz quality."},
        {"level": "professional", "prompt": "Electronic launch render — true wireless earbuds in charging case. Materials: polished gloss + soft-touch matte mix. Lighting: studio 3-point (key/fill/rim). Composition: clean floating hero shot. Background: dark gradient with subtle ambient occlusion. Output: 6K photorealistic (Keyshot)."},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Luxury watch viz — Swiss automatic movement visible through sapphire caseback. Materials: 18k gold case, guilloché dial with hand-engraving, bracelet micro-scratches (displacement map). Lighting: HDRI gem studio with spectral caustics for diamond indices. Detail: sub-millimetre precision. Output: 16K, CGI-to-photo indistinguishable."},
        {"level": "expert", "prompt": "EV concept — electric auto-rickshaw redesign (2040 India). Modelling: parametric surfaces. Materials: iridescent paint with flake simulation, neon underglow. Lighting: physically accurate headlight IES profiles. Engine: Unreal Engine 5 Lumen (real-time ray tracing). Output: 4K 60fps interactive walkthrough + pre-rendered beauty shots."},
    ],
}

# ─── DESIGN BRIEF SYSTEM PROMPT ──────────────────────────────────────────────────
DESIGN_BRIEF_SYSTEM_PROMPT = """You are an expert design brief consultant specializing in transforming creative concepts into comprehensive, production-ready design specifications.

Your task: Take the user's design concept/content and transform it into a detailed design brief with multiple professional variations.

**OUTPUT STRUCTURE** — Generate 3 design brief variations with these sections for EACH:

For each variation, provide:
1. **Design Brief Title** (e.g., "Elegant & Luxe", "Modern & Vibrant", "Artisan & Warm")
2. **Core Message / Content Integration** — How the full user message is incorporated
3. **Project Requirements** — Resolution, format, technical specs
4. **Visual Style** — Design aesthetic direction
5. **Color Palette** — 3-4 specific colors with hex codes and names
6. **Typography** — Font families and hierarchy
7. **Key Design Elements** — Specific visual components to include
8. **Composition** — Layout strategy and visual hierarchy
9. **Deliverables** — Exact file formats and variants
10. **Tools Recommended** — Specific software/platforms

**IMPORTANT RULES**:
- Include ALL user content and messaging in the brief (not a summary—preserve the actual text/emojis they provided)
- Provide 3 DISTINCT creative directions, NOT variations of the same brief
- Make each brief ready for a designer to execute immediately
- Use professional design terminology
- Include specific, actionable details (hex codes, pixel dimensions, font names)
- Keep each variation focused but comprehensive

Return response as valid JSON:
```json
{
  "briefs": [
    {
      "title": "Brief Title",
      "core_message": "Full integration of user content",
      "requirements": "Technical specs",
      "visual_style": "Design direction",
      "color_palette": [{"name": "Color", "hex": "#000000"}],
      "typography": "Font specifications",
      "key_elements": ["Element 1", "Element 2"],
      "composition": "Layout strategy",
      "deliverables": "File formats",
      "tools": ["Software 1", "Software 2"]
    }
  ]
}
```"""

# ─── CATEGORY METADATA ────────────────────────────────────────────────────────
CATEGORY_META = {
    "general_photography":  {"emoji": "📷", "tools": ["Lightroom", "Photoshop"], "best_for": "Instagram feed, portfolio"},
    "women_professional":   {"emoji": "👩‍💼", "tools": ["DALL-E 3", "Midjourney"], "best_for": "Profile photos, fashion"},
    "women_transform":      {"emoji": "✨", "tools": ["DALL-E 3", "Stable Diffusion"], "best_for": "Transformation content"},
    "men_professional":     {"emoji": "👨‍💼", "tools": ["DALL-E 3", "Midjourney"], "best_for": "Profile photos, fashion"},
    "men_transform":        {"emoji": "💪", "tools": ["DALL-E 3", "Stable Diffusion"], "best_for": "Transformation content"},
    "couples_general":      {"emoji": "💑", "tools": ["DALL-E 3", "Midjourney"], "best_for": "Pre-wedding, lifestyle"},
    "couples_transform":    {"emoji": "💕", "tools": ["DALL-E 3", "Stable Diffusion"], "best_for": "Couple transformation"},
    "design_posters":       {"emoji": "🎨", "tools": ["Canva", "Photoshop", "DALL-E 3"], "best_for": "Social media graphics, print"},
    "reel_scripts":         {"emoji": "🎬", "tools": ["CapCut", "Premiere Pro"], "best_for": "Instagram Reels, TikTok"},
    "captions_templates":   {"emoji": "✍️", "tools": ["ChatGPT", "Notion"], "best_for": "Instagram captions"},
    "email_subjects":       {"emoji": "📧", "tools": ["Mailchimp", "Notion"], "best_for": "Email marketing"},
    "ui_ux_design":         {"emoji": "🖥️", "tools": ["Figma", "Adobe XD", "Sketch"], "best_for": "App & web design"},
    "brand_identity":       {"emoji": "🏷️", "tools": ["Illustrator", "Figma", "Looka"], "best_for": "Logos, branding, identity"},
    "illustration_art":     {"emoji": "🖌️", "tools": ["Procreate", "Illustrator", "Midjourney"], "best_for": "Digital art, editorial"},
    "animation_motion":     {"emoji": "🎞️", "tools": ["After Effects", "Lottie", "Rive"], "best_for": "Motion graphics, reels"},
    "photography_styles":   {"emoji": "📸", "tools": ["Lightroom", "Capture One", "Photoshop"], "best_for": "Fine art, editorial"},
    "print_design":         {"emoji": "🖨️", "tools": ["InDesign", "Photoshop", "Canva"], "best_for": "Flyers, packaging, books"},
    "product_3d":           {"emoji": "📦", "tools": ["Blender", "Cinema 4D", "Keyshot"], "best_for": "Product launch, e-commerce"},
}

DIFFICULTY_EMOJI = {"beginner": "🟢", "professional": "🔵", "expert": "🔴"}


def get_prompt(category: str, index: int = 0, level: str = None) -> str:
    """Get a specific prompt. If level given, filter by difficulty first."""
    prompts = get_category_prompts(category, level)
    if prompts and index < len(prompts):
        p = prompts[index]
        return p["prompt"] if isinstance(p, dict) else p
    return get_category_prompts("general_photography")[0]


def list_categories() -> list:
    """Return all category names."""
    return list(PROMPTS.keys())


def get_all_prompts_count() -> int:
    """Total number of prompts across all categories."""
    total = 0
    for v in PROMPTS.values():
        total += len(v)
    return total


def get_category_prompts(category: str, level: str = None) -> list:
    """
    Get prompts for a category.
    If level is 'beginner', 'professional', or 'expert', filter by that level.
    Old-format string prompts (legacy) are always included when no level filter.
    """
    raw = PROMPTS.get(category, [])
    if not raw:
        return []

    # Legacy format (plain strings)
    if isinstance(raw[0], str):
        return raw

    # New format (list of dicts with "level" and "prompt")
    if level and level in ("beginner", "professional", "expert"):
        return [item for item in raw if item.get("level") == level]

    return raw


def get_prompts_by_level(category: str, level: str) -> list[str]:
    """Return prompt strings for a category filtered by level."""
    items = get_category_prompts(category, level)
    result = []
    for item in items:
        if isinstance(item, dict):
            result.append(item["prompt"])
        else:
            result.append(item)
    return result


def get_category_meta(category: str) -> dict:
    """Return metadata (emoji, tools, best_for) for a category."""
    return CATEGORY_META.get(category, {"emoji": "🎯", "tools": [], "best_for": "General use"})


def search_prompts(keyword: str) -> list[dict]:
    """Search all prompts for a keyword. Returns list of {category, level, prompt}."""
    keyword = keyword.lower()
    results = []
    for cat, items in PROMPTS.items():
        for item in items:
            if isinstance(item, dict):
                if keyword in item["prompt"].lower():
                    results.append({"category": cat, "level": item.get("level", ""), "prompt": item["prompt"]})
            else:
                if keyword in item.lower():
                    results.append({"category": cat, "level": "", "prompt": item})
    return results

