"""300+ Prompt Templates Library — Photography, Design, UI/UX, Branding, Illustration, Animation, Print, 3D"""

# Difficulty levels per category: "beginner" | "professional" | "expert"
# Use get_category_prompts(category, level) to filter by difficulty.

PROMPTS = {
    # CATEGORY A: GENERAL PHOTOGRAPHY
    "general_photography": [
        "Subject: Young Indian professional in traditional kurta with modern styling. Lighting: soft natural window light with bokeh background. Pose: confident professional stance. Expression: direct engaging eye contact. Style: modern editorial photography. Camera: shallow depth of field, slightly above eye level.",
        
        "Subject: Indian family having chai on rooftop. Lighting: golden-hour warm glow. Pose: natural candid interaction, relaxed sitting. Expression: genuine moments, warm connection. Style: authentic lifestyle photography. Background: city skyline blurred softly. Camera: natural framing, soft warm tones.",
        
        "Subject: Indian marketplace with traditional vendors. Lighting: natural daylight, warm tones. Pose: vendors in natural work positions. Expression: authentic engagement. Style: documentary street photography. Background: vibrant marketplace stalls, colorful textiles. Camera: sharp detail with intentional depth.",
        
        "Subject: Indian woman in designer saree with traditional jewelry. Lighting: studio key-fill lighting, no harsh shadows. Pose: poised editorial stance. Expression: confident engaging gaze. Style: high-fashion editorial aesthetic. Camera: sharp focus, professional framing, flattering angle.",
        
        "Subject: Indian temple architecture with ancient stonework. Lighting: dramatic golden-hour illumination. Pose: architectural composition. Style: fine-art architectural photography. Background: intricate stone details in warm light. Camera: wide-angle composition emphasizing scale and detail.",
    ],
    
    # CATEGORY B: WOMEN'S PHOTOSHOOT
    "women_professional": [
        "Subject: Indian woman in modern office wear. Lighting: studio lighting, neutral background. Pose: confident professional stance, one hand on desk. Expression: direct eye contact, confident presence. Style: corporate aesthetic. Camera: professional headshot angle.",
        
        "Subject: Indian woman in elegant traditional saree with jewelry. Lighting: studio key-fill lighting. Pose: graceful stance with natural arm placement. Expression: serene sophisticated gaze. Style: glamour photography. Background: neutral clean backdrop.",
        
        "Subject: Young Indian woman in casual modern outfit. Lighting: natural outdoor light, garden setting. Pose: relaxed approachable stance. Expression: warm engaging smile. Style: lifestyle photography. Background: soft park/garden environment.",
        
        "Subject: Indian woman in fusion wear (saree + leather jacket). Lighting: urban natural light. Pose: edgy confident power stance. Expression: modern assured presence. Style: fashion editorial. Background: urban setting.",
        
        "Subject: Indian woman in traditional bridal wear with ornate jewelry. Lighting: dramatic warm studio lighting. Pose: regal seated or standing posture. Expression: radiant dignified presence. Style: wedding glamour photography. Camera: elevated composition.",
        
        "Subject: Indian woman in beach/tropical outfit. Lighting: golden-hour warm glow. Pose: confident relaxed stance. Expression: warm engaging smile. Style: lifestyle photography. Background: tropical/beach environment.",
        
        "Subject: Young Indian woman in fitness wear in active stance. Lighting: motivational studio lighting. Pose: dynamic athletic positioning. Expression: powerful energetic presence. Style: fitness aesthetic. Background: fitness environment.",
        
        "Subject: Indian woman in ethnic wear (anarkali/lehenga) with traditional jewelry. Lighting: festive warm lighting. Pose: celebratory graceful stance. Expression: joyful radiant smile. Style: traditional celebration aesthetic. Background: festive environment.",
    ],
    
    "women_transform": [
        "Subject: Indian woman in formal corporate office wear. Identity: Maintain natural likeness from reference image. Keep natural facial proportions. Pose: Standing tall with shoulders back, one hand on desk, head slightly tilted upward. Expression: Confident direct eye contact. Style: Corporate professional aesthetic. Lighting: Studio key-fill lighting. Background: Professional office environment. Camera: Confident headshot angle with shallow depth of field.",
        
        "Subject: Indian woman in elegant traditional silk saree. Identity: Maintain natural likeness from reference image. Pose: Standing gracefully with one shoulder forward, hand on chest, three-quarters body angle. Expression: Soft serene sophisticated gaze. Style: Glamour photography aesthetic. Lighting: Studio glamour lighting. Background: Neutral elegant backdrop. Camera: Professional pose with flattering angle.",
        
        "Subject: Young Indian woman in modern fusion wear (traditional meets contemporary). Identity: Maintain natural likeness from reference image. Pose: Dynamic power pose, one leg forward, confident strong stance. Expression: Modern confident presence. Style: High-fashion editorial aesthetic. Lighting: Professional editorial lighting. Background: Professional lighting setup.",
        
        "Subject: Indian bride in traditional bridal wear (ornate lehenga/saree). Identity: Maintain natural likeness from reference image. Pose: Regal posture, one hand raised showing jewelry, seated or standing. Expression: Dignified radiant presence. Style: Wedding celebration aesthetic. Lighting: Dramatic warm studio lighting. Background: Wedding celebration environment.",
        
        "Subject: Indian woman as lifestyle influencer. Identity: Maintain natural likeness from reference image. Pose: Candid walking pose with natural arm movement, confident stride. Expression: Engaging warm smile toward camera. Style: Contemporary lifestyle aesthetic. Lighting: Natural warm lighting. Background: Lifestyle environment with Instagram appeal.",
        
        "Subject: Indian woman with professional glamour aesthetic. Identity: Maintain natural likeness from reference image. Pose: Seated or reclined in magazine-worthy pose, one arm extended gracefully. Expression: Confident luxurious presence. Style: Luxury beauty photography. Lighting: Professional beauty studio lighting. Background: Dramatic professional setting.",
        
        "Subject: Fit Indian woman in gym/fitness wear. Identity: Maintain natural likeness from reference image. Pose: Dynamic athletic pose, one leg extended, arms flexed. Expression: Powerful energetic presence. Style: Fitness model aesthetic. Lighting: Motivational studio lighting. Background: Fitness environment.",
        
        "Subject: Indian woman in traditional wedding ceremony ethnic wear. Identity: Maintain natural likeness from reference image. Pose: Standing with hands in traditional position, celebratory posture. Expression: Joyful radiant smile. Style: Traditional celebration aesthetic. Lighting: Festive warm ceremonial lighting. Background: Celebration environment.",
        
        "Subject: Indian woman as Bollywood celebrity. Identity: Maintain natural likeness from reference image. Pose: Dramatic pose leaning against surface, one leg bent, theatrical hand placement. Expression: Expressive confident cinematic presence. Style: Cinema-quality photography. Lighting: Dramatic red carpet lighting. Background: Theatrical professional backdrop.",
        
        "Subject: Indian woman as travel influencer. Identity: Maintain natural likeness from reference image. Pose: Adventurous action pose (standing on viewpoint, exploring), looking toward horizon. Expression: Adventurous engaged presence. Style: Travel adventure aesthetic. Lighting: Natural golden-hour lighting. Background: Exotic destination landscape.",
    ],
    
    # CATEGORY C: MEN'S PHOTOSHOOT
    "men_professional": [
        "Subject: Indian man in formal business suit. Lighting: studio professional lighting. Pose: confident professional stance, power positioning. Expression: direct eye contact, commanding presence. Style: corporate executive aesthetic. Camera: professional headshot angle.",
        
        "Subject: Young Indian man in traditional ethnic wear (kurta pajama). Lighting: studio warm lighting. Pose: dignified standing posture. Expression: focused sophisticated gaze. Style: cultural aesthetic. Background: clean professional backdrop.",
        
        "Subject: Indian man in casual smart wear (shirt + jeans). Lighting: natural outdoor lighting. Pose: relaxed approachable stance. Expression: warm engaging smile. Style: lifestyle photography. Background: natural environment.",
        
        "Subject: Fit Indian man in gym wear/fitness clothing. Lighting: motivational studio lighting. Pose: athletic power stance. Expression: strong energetic presence. Style: fitness model aesthetic. Background: fitness environment.",
        
        "Subject: Indian man in traditional festival wear (dhoti, sherwani). Lighting: golden warm festive lighting. Pose: celebratory dignified stance. Expression: proud warm presence. Style: traditional celebration aesthetic. Background: festive environment.",
        
        "Subject: Young Indian man in streetwear/urban fashion. Lighting: natural urban lighting. Pose: trendy confident stance. Expression: modern engaged presence. Style: contemporary fashion aesthetic. Background: urban setting.",
        
        "Subject: Indian man in semi-formal Indian ethnic wear (Nehru jacket with traditional elements). Lighting: studio professional lighting. Pose: sophisticated poised stance. Expression: elegant composed presence. Style: refined elegant aesthetic. Camera: professional flattering angle.",
        
        "Subject: Indian man in traditional South Indian wear (veshti, traditional top). Lighting: warm cultural lighting. Pose: cultural dignified posture. Expression: authentic cultural presence. Style: traditional authentic aesthetic. Background: cultural environment.",
    ],
    
    "men_transform": [
        "Subject: Indian man in formal business suit. Identity: Maintain natural likeness from reference image. Pose: Standing tall with hands in power position, commanding confidence. Expression: Direct eye contact, executive presence. Style: Corporate professional aesthetic. Lighting: Studio professional lighting. Background: Professional office environment.",
        
        "Subject: Handsome Indian man in traditional kurta pajama. Identity: Maintain natural likeness from reference image. Pose: Standing gracefully with one hand on chest, dignified posture. Expression: Soft focused sophisticated gaze. Style: Cultural aesthetic. Lighting: Studio elegant lighting. Background: Professional backdrop.",
        
        "Subject: Athletic Indian man in gym wear. Identity: Maintain natural likeness from reference image. Pose: Dynamic power pose with arms flexed, strong confident stance. Expression: Powerful energetic presence. Style: Fitness model aesthetic. Lighting: Motivational fitness lighting. Background: Fitness environment.",
        
        "Subject: Glamorous Indian man as Bollywood actor. Identity: Maintain natural likeness from reference image. Pose: Dramatic pose leaning against surface, one hand raised. Expression: Intense engaged eye contact, confident presence. Style: Cinema-quality photography. Lighting: Dramatic professional lighting. Background: Theatrical professional setting.",
        
        "Subject: Trendy Indian man as lifestyle influencer. Identity: Maintain natural likeness from reference image. Pose: Relaxed confident standing pose, one hand in pocket. Expression: Engaging warm smile toward camera. Style: Contemporary lifestyle aesthetic. Lighting: Natural warm lighting. Background: Instagram-worthy lifestyle environment.",
        
        "Subject: Indian man in traditional festival wear (sherwani, ethnic). Identity: Maintain natural likeness from reference image. Pose: Standing regal with hands gracefully placed. Expression: Celebratory proud warm presence. Style: Festive celebration aesthetic. Lighting: Golden warm festive lighting. Background: Celebration environment.",
        
        "Subject: Indian man as travel influencer. Identity: Maintain natural likeness from reference image. Pose: Adventurous action pose (standing on mountain, exploring), looking toward horizon. Expression: Adventurous engaged presence. Style: Adventure aesthetic. Lighting: Natural golden-hour lighting. Background: Exotic destination landscape.",
        
        "Subject: Artistic creative Indian man. Identity: Maintain natural likeness from reference image. Pose: Sophisticated pose leaning or seated artistically. Expression: Thoughtful composed cultured presence. Style: Creative professional aesthetic. Lighting: Artistic professional lighting. Background: Creative artistic environment.",
        
        "Subject: Luxury lifestyle Indian man. Identity: Maintain natural likeness from reference image. Pose: Standing confidently in premium designer wear. Expression: Sophisticated composed elegant presence. Style: Luxury aesthetic. Lighting: Sophisticated professional lighting. Background: High-end upscale environment.",
        
        "Subject: Charismatic Indian man for dating profile. Identity: Maintain natural likeness from reference image. Pose: Relaxed approachable pose with gentle presence. Expression: Welcoming engaging direct eye contact. Style: Approachable romantic aesthetic. Lighting: Warm romantic lighting. Background: Warm professional backdrop.",
    ],
    
    # CATEGORY D: COUPLES
    "couples_general": [
        "Subject: Indian couple in pre-wedding romantic setting. Lighting: golden-hour warm glow. Pose: close comfortable stance, leaning toward each other. Expression: warm romantic connection. Style: pre-wedding aesthetic. Background: outdoor garden environment. Camera: shallow depth of field emphasizing couple.",
        
        "Subject: Indian couple in traditional wedding attire (bride in lehenga, groom in sherwani). Lighting: warm festive ceremonial lighting. Pose: regal close stance. Expression: joyful celebratory presence. Style: wedding celebration aesthetic. Background: traditional wedding environment.",
        
        "Subject: Young Indian couple in casual modern outfit. Lighting: natural warm lighting. Pose: candid relaxed stance, natural connection. Expression: genuine authentic smiles. Style: lifestyle photography. Background: park/garden environment.",
        
        "Subject: Indian couple in ethnic fusion wear (traditional meets contemporary). Lighting: natural professional lighting. Pose: comfortable close stance. Expression: modern confident presence. Style: contemporary fashion aesthetic. Background: professional setting.",
        
        "Subject: Couple in traditional festival outfit (Holi celebration). Lighting: bright festive lighting with colored powders. Pose: playful energetic close stance. Expression: joyful playful celebration. Style: festive celebration aesthetic. Background: festive environment.",
        
        "Subject: Indian couple in formal ethnic wear (woman in saree, man in formal kurta). Lighting: studio professional lighting. Pose: elegant close stance. Expression: sophisticated composed presence. Style: formal ethnic aesthetic. Background: professional backdrop.",
        
        "Subject: Young couple in beach/casual wear. Lighting: golden-hour sunset glow. Pose: romantic relaxed walking together. Expression: intimate connected presence. Style: vacation lifestyle aesthetic. Background: coastal landscape.",
        
        "Subject: Couple during Indian wedding ceremony (bride in bridal saree, groom in sherwani). Lighting: warm ceremonial lighting. Pose: ceremonial close connection. Expression: sacred joyful presence. Style: wedding ceremony aesthetic. Background: temple/ceremony setting.",
    ],
    
    "couples_transform": [
        "Subject: Couple portrait using two reference images. Identity: Maintain natural likeness of both individuals. Keep both identities distinct. Use both reference images equally weighted. Pose: Standing close, slightly leaning toward each other. Fingers intertwined. Her right hand on his shoulder, his right hand holding hers. Head: Soft tilt toward each other (~45°). Expression: Warm subtle romantic smiles. Style: 90s vintage fashion aesthetic. Lighting: Warm soft cinematic lighting with golden-hour tone. Background: Blurred vintage cityscape or soft gradient. Camera: Slightly above eye level, shallow depth of field.",
        
        "Subject: Indian couple pre-wedding photoshoot using two reference images. Identity: Maintain natural likeness of both individuals from reference images. Keep distinct facial characteristics. Pose: Bride facing forward, groom standing behind with arms around bride, both turning toward camera. Expression: Warm romantic connection and engagement. Style: Pre-wedding aesthetic. Lighting: Softbox with golden hour glow. Background: Outdoor garden with natural environment. Camera: Shallow depth of field emphasizing couple connection.",
        
        "Subject: Indian wedding couple portrait using two reference images. Identity: Maintain natural likeness for both subjects from reference images. Preserve individual features. Pose: Bride and groom facing each other, joyful expressions, gentle body connection. Attire: Bride in bridal saree/lehenga, groom in traditional sherwani. Expression: Joyful romantic celebration. Style: Wedding celebration aesthetic. Lighting: Warm golden ceremonial lighting. Background: Temple or ceremonial backdrop. Camera: Centered composition, slight elevated angle.",
        
        "Subject: Engaged Indian couple using two reference images. Identity: Maintain natural likeness of both individuals from references. Keep facial characteristics distinct. Pose: Couple seated close together, hands intertwined, facing camera. Expression: Romantic intimate connection. Style: Engagement photography aesthetic. Lighting: Professional studio setup with soft directional light. Background: Studio environment with neutral background. Attire: Formal elegant wear.",
        
        "Subject: Indian couple celebrating anniversary using two reference images. Identity: Maintain natural likeness of both individuals from reference images. Pose: Standing facing each other with warm embrace. Expression: Joyful celebratory connection. Style: Romantic celebration aesthetic. Lighting: Warm candlelight with subtle key light. Background: Romantic dining environment with candlelight ambiance. Attire: Formal elegant wear.",
        
        "Subject: Couple on honeymoon vacation using two reference images. Identity: Maintain natural likeness of both individuals from references. Pose: Walking hand in hand toward horizon. Expression: Relaxed joyful presence. Style: Travel adventure aesthetic. Lighting: Golden-hour sunset glow. Background: Exotic tropical landscape with sunset. Camera: Full-body composition with landscape context.",
        
        "Subject: Indian couple celebrating Holi festival using two reference images. Identity: Maintain natural likeness of both individuals from references. Pose: Playfully posing together with colored powder in air. Expression: Energetic joyful playful presence. Style: Festive celebration aesthetic. Lighting: Bright festive lighting with colored powder effects. Background: Outdoor festive environment. Camera: Dynamic action composition.",
        
        "Subject: Couple on romantic dinner date using two reference images. Identity: Maintain natural likeness of both individuals from references. Pose: Seated at table, leaning toward each other, intimate eye contact. Expression: Warm loving connected presence. Style: Intimate romantic aesthetic. Lighting: Candlelight with warm accent lighting. Background: Elegant restaurant environment. Attire: Formal elegant wear.",
        
        "Subject: Modern Indian couple as influencers using two reference images. Identity: Maintain natural likeness of both individuals from references. Pose: Back-to-back, both looking toward camera with confident relaxed expressions. Expression: Confident contemporary presence. Style: Modern lifestyle aesthetic. Lighting: Natural warm professional lighting. Background: Urban or contemporary setting. Camera: Full-body composition showing style.",
        
        
        "Subject: Couple in travel adventure using two reference images. Identity: Maintain natural likeness of both individuals from references. Pose: Sitting together looking at landscape/destination, intimate connected pose. Expression: Adventurous joyful engaged presence. Style: Adventure lifestyle aesthetic. Lighting: Golden-hour natural lighting. Background: Exotic destination landscape. Camera: Landscape-oriented composition.",
        
        "Subject: Luxury lifestyle Indian couple using two reference images. Identity: Maintain natural likeness of both individuals from references. Pose: Standing together facing forward, confident elegant posture. Expression: Sophisticated composed presence. Style: Luxury upscale aesthetic. Lighting: Sophisticated professional lighting. Background: High-end upscale environment. Attire: Premium designer wear.",
    ],
    
    # CATEGORY F: DESIGN & POSTERS
    "design_posters": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Motivational Instagram post. Typography: bold white text on dark gradient. Elements: simple geometric shapes. Layout: clean modern centered. Format: 1080x1080px"},
        {"level": "beginner", "prompt": "Diwali festival graphic. Colors: gold and red accents. Element: diya illustration centered. Text: festive typography. Format: Instagram square 1080x1080"},
        {"level": "beginner", "prompt": "Fitness quote poster. Background: dark gym aesthetic. Text: bright accent typography, bold sans-serif. Icon: simple motivational graphic. Format: Instagram story 1080x1920"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Minimalist motivational poster. Layout: grid-based composition. Typography: bold sans-serif headline. Pattern: geometric Rangoli-inspired inspiration. Colors: deep navy + saffron contrast. Style: modern flat design. Format: 1920x1080 300dpi print"},
        {"level": "professional", "prompt": "Holi festival social graphic. Colors: dynamic magenta, cyan, yellow splash. Layout: rule-of-thirds with photo overlay. Typography: editorial modern sans-serif. Style: vibrant motion aesthetic. Format: 1080x1350 Instagram portrait"},
        {"level": "professional", "prompt": "Women empowerment poster. Subject: strong silhouette of Indian woman. Colors: duotone purple/gold palette. Layout: negative space composition. Typography: editorial hierarchy. Format: 1080x1350 Instagram optimized"},
        {"level": "professional", "prompt": "Travel destination carousel. Content: golden-hour landmark photography. Layout: magazine-style with white space. Typography: elegant serif headline + body. Format: 1080x1080 carousel 300dpi"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Avant-garde conceptual poster. Concept: Mughal architecture + cyberpunk neon blend. Technique: glitch art with chromatic aberration. Grid: brutalist composition. Typography: custom variable font. Format: 4K 3840x2160 with bleed"},
        {"level": "expert", "prompt": "Luxury brand announcement. Layout: ultra-minimal floating hero product. Material: marble texture background. Effect: gold foil emboss simulation. Typography: Swiss sans-serif precision. Grid: 5pt measurement. Format: A2 print 420x594mm 300dpi CMYK"},
        {"level": "expert", "prompt": "Premium financial infographic. Style: dark glass-morphism panels with neon data visualizations. Data: interactive sortable elements. Typography: hierarchical sans-serif scale. Format: 1920x1080 UHD for web + print"},
    ],

    # CATEGORY G: REEL SCRIPTS
    "reel_scripts": [
        {"level": "beginner", "prompt": "15-second morning routine Reel. Hook: warm lighting establishing shot. Content: 3 simple sequential steps. Style: soft background music. Text: overlay labels for each step. Format: vertical 9:16"},
        {"level": "beginner", "prompt": "30-second transformation Reel. Structure: before/after split-screen. Transition: smooth wipe effect. Audio: trending sound. Text: motivational overlay. Format: vertical 9:16"},
        {"level": "beginner", "prompt": "15-second relatable POV Reel. Concept: everyday Indian life moment. Location: single continuous setting. Audio: trending sound. Text: one caption. Format: vertical 9:16"},
        {"level": "professional", "prompt": "30-second educational Reel. Hook: attention-grabbing (0-2s). Content: 'Did You Know' Indian history fact. Visuals: kinetic text overlays with 4-cut sequence. Audio: royalty-free upbeat tempo. CTA: end-screen engagement. Format: vertical 9:16"},
        {"level": "professional", "prompt": "45-second day-in-life Reel. Structure: Indian entrepreneur morning routine. Editing: 6-cut sequence with smooth transitions. Aesthetic: golden-hour warm color. Audio: voiceover narration. Labels: lower-third identifier text. Format: vertical 9:16"},
        {"level": "professional", "prompt": "30-second product reveal Reel. Reveal: dramatic lighting reveal moment. Content: slow-motion product detail shots. Audio: trending sound matched to beat. Branding: logo sting at end. Format: vertical 9:16"},
        {"level": "expert", "prompt": "60-second cinematic brand story Reel. Production: 4K footage with film emulation color grade. Editing: jump-cuts synced to bass drops. Typography: motion-tracked text animations. Aspect: dynamic ratio transitions (16:9→9:16). Grade: cohesive brand color science. Format: 4K for all platforms"},
        {"level": "expert", "prompt": "45-second viral challenge Reel. Concept: original Indian cultural twist on global trend. Production: multi-location shoot with drone intro. Editing: match-cut rhythm transitions. Animation: waveform-synced text effects. CTA: interactive sticker engagement. Format: vertical 9:16 optimized"},
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
        {"level": "professional", "prompt": "[First Name], Your Personalized Growth Plan Is Ready"},
        {"level": "expert", "prompt": "The algorithm-proof content framework top 1% creators use (never shared publicly)"},
        {"level": "expert", "prompt": "Why your reach dropped 40% last month — and the exact fix 3 creators used to bounce back"},
    ],

    # ─── NEW CATEGORY 1: UI/UX DESIGN ─────────────────────────────────────────
    "ui_ux_design": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Mobile app login screen. Elements: email/password fields, login button. Style: clean white background, blue primary button, iOS-style. Format: Figma mockup"},
        {"level": "beginner", "prompt": "Simple analytics dashboard. Layout: card-based stat tiles (4 cards). Background: light grey. Typography: clean sans-serif. Approach: mobile-first design"},
        {"level": "beginner", "prompt": "E-commerce product page. Layout: product image left, details right. CTA: prominent 'Add to Cart' button. Style: minimal responsive design"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Fitness iOS app onboarding (screen 3/5). Feature: animated progress ring (saffron/teal). Layout: dark theme. Typography: SF Pro Display. Interaction: bottom sheet micro-animation. Specs: safe-area layout, WCAG AA contrast, 390x844px @3x"},
        {"level": "professional", "prompt": "SaaS analytics dashboard. Layout: glass-morphism sidebar + gradient area charts. Content: sortable data table. Theme: dark mode. Typography: Inter. Grid: 8pt spacing. Breakpoint: 1440px desktop. Components: Figma auto-layout"},
        {"level": "professional", "prompt": "Food delivery app home. Layout: card grid of restaurants, sticky search. Filters: category pills for browsing. Loading: skeleton state. Design: Material You colors. Specs: 360x800 Android, 4dp corner radius system"},
        {"level": "professional", "prompt": "FinTech wallet app transaction history. Layout: timeline list with category icons. Colors: income green/expense red accent. Feature: mini sparkline chart per transaction. Navigation: bottom nav bar. Standard: iOS Human Interface Guidelines"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "AI productivity app command palette. Features: frosted glass blur (backdrop-filter 20px), animated type-ahead with confidence scoring, keyboard shortcuts. Design: tokenized system variables, dark/light adaptive. Accessibility: WCAG AAA. Tools: Figma variables + modes"},
        {"level": "expert", "prompt": "Luxury real-estate web app. Hero: full-bleed 3D property viewer. UI: spatial floating controls, cinematic parallax scroll. Typography: editorial serif + geometric sans mix. Grid: 12-column 1920px. Animation: Lottie + Framer Motion micro-system"},
        {"level": "expert", "prompt": "Enterprise B2B data platform complex table. Features: inline editing, multi-select bulk actions, contextual command bar, resizable columns, drag-to-reorder. Filters: advanced AND/OR logic builder. Accessibility: ARIA live regions, focus trap management. Docs: Storybook library"},
    ],

    # ─── NEW CATEGORY 2: BRAND IDENTITY ───────────────────────────────────────
    "brand_identity": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Indian food brand logo. Style: round badge. Colors: warm orange and brown. Element: fork and leaf icon. Typography: clean sans-serif"},
        {"level": "beginner", "prompt": "Wellness brand color palette. Swatches: 5 colors. Colors: earthy greens and creams. Format: labeled hex codes"},
        {"level": "beginner", "prompt": "Social media profile kit. Components: profile picture + banner. Style: consistent colors and fonts. Platform: Instagram"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Premium ayurvedic wellness brand. Logo: elegant serif (Garamond) + lotus monogram. Palette: ivory, forest green, burnished gold. Lockups: primary + secondary. Guidelines: minimum size, clear-space. Format: A4 brand sheet"},
        {"level": "professional", "prompt": "D2C Indian fashion brand identity. Pattern: geometric batik-inspired system. Typography: display + body typeface pair. Palette: 6 colors with usage ratios. Logos: light/dark/pattern versions. Packaging: garment tag + shopping bag mockups"},
        {"level": "professional", "prompt": "Tech startup brand kit. Logo: bold geometric wordmark. Icons: 6 custom SVG set. Palette: blue-violet + neutrals. Typography: Inter + Space Grotesk. Stationery: business card, letterhead, email signature. Tools: Figma brand tokens"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Heritage luxury jewellery brand rebrand. Logo: custom variable serif with optical weight. Pattern: micro-Bidriware metalwork inspired. Colors: 3-tier system (hero/supporting/accent). Print: holographic foil simulation. Innovation: adaptive logo for AR. Deliverable: 60-page brand book"},
        {"level": "expert", "prompt": "Global fintech brand system. Logo: responsive family (full/compact/icon/favicon). Typography: multilingual (Latin + Devanagari + Arabic). Colors: semantic token architecture (global→alias→component). Motion: easing curves + timing. Audit: accessibility compliance. Export: Figma Tokens JSON"},
    ],

    # ─── NEW CATEGORY 3: ILLUSTRATION & DIGITAL ART ───────────────────────────
    "illustration_art": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Cute flat illustration. Subject: Indian street food cart. Style: bright colors, simple shapes, no shadows, vector. Background: white"},
        {"level": "beginner", "prompt": "Character illustration. Subject: Indian woman in saree. Style: bold outline, flat color fill, kawaii proportions. Technique: digital art"},
        {"level": "beginner", "prompt": "Minimal line art. Subject: Indian city skyline. Style: single color, thin strokes, silhouetted landmarks. Use: t-shirt print"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Editorial illustration — Indian woman coder. Style: holographic UI elements, isometric perspective. Palette: vibrant jewel tones. Technique: Procreate digital with textured grain. Output: 2400x1600px"},
        {"level": "professional", "prompt": "Children's book illustration. Scene: Indian village festival at night. Focus: Diwali lamps reflected in river. Technique: warm painterly gouache. Style: soft lighting, rich storytelling. Output: 3000x2000px 300dpi"},
        {"level": "professional", "prompt": "Concept art — Indian mythology character (Arjuna as modern archer hero). Pose: dynamic action, detailed Mahabharata-inspired armor. Lighting: dramatic rim-light. Technique: painterly rendering. Output: 2K square"},
        {"level": "professional", "prompt": "Infographic illustration — Indian spice market. Elements: 8 spice icons with hand-drawn linework + watercolor texture. Labels: editorial serif fonts. Palette: warm earthy tones. Format: A3 print"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Surrealist digital painting. Concept: Indian classical dancer transforming into cosmic deity. Details: body formed from micro-marigolds. Palette: terracotta→celestial indigo gradient. Technique: individual petal rendering (Beeple-level detail). Output: 8K UHD"},
        {"level": "expert", "prompt": "Graphic novel cover — dystopian Mumbai 2087. Palette: acid yellow/noir black/rust orange. Technique: ink-wash + digital hybrid with atmospheric haze. Composition: cyberpunk characters (foreground)→broken architecture (midground)→blood-red sky. Format: 210x297mm A4 bleed. Style: Frank Miller influence"},
        {"level": "expert", "prompt": "Generative mandala. Algorithm: parametric symmetry composed from Tamil Kolam patterns. Structure: 256-color HSL gradient spectrum. Detail: ultra-fine linework at 0.1pt. Output: large-format canvas 120x120cm at 300dpi"},
    ],

    # ─── NEW CATEGORY 4: ANIMATION & MOTION GRAPHICS ─────────────────────────
    "animation_motion": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Logo reveal animation. Effect: fade-in with subtle scale. Duration: 2 seconds. Background: white. Timing: ease-in-out. Output: GIF + MP4"},
        {"level": "beginner", "prompt": "Instagram story text animation. Content: bold headline revealing word by word. Background: colorful. Duration: 5 seconds loop. Style: After Effects template"},
        {"level": "beginner", "prompt": "Loading spinner. Element: circular progress ring in brand color. Timing: smooth 1-second loop. Background: transparent. Format: Lottie JSON"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Brand intro sting (3-sec). Animation: wordmark assembled by particle swarm. Background: deep blue. Effect: subtle lens flare. Audio: synced to logo hit beat. Tool: After Effects. Output: 1920x1080 ProRes"},
        {"level": "professional", "prompt": "Animated explainer (30-sec) — UPI payment flow. Style: flat 2D with smooth transitions, kinetic typography. Audio: royalty-free upbeat. Market: India-focused. Output: 1080x1920 vertical + 1920x1080 horizontal"},
        {"level": "professional", "prompt": "Social carousel animation. Content: 5-slide product launch sequence. Motion: consistent transitions (slide-in left, scale pop). Colors: brand palette. Export: GIF + MP4 auto-advancing. Format: 1080x1080 24fps"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Title sequence — Indian web series. Technique: hand-drawn frame-by-frame animation. Content: mythological→modern urban transition. Frame rate: 12fps artistic stagger. Texture: traditional miniature painting inspiration. Audio: orchestral + electronic blend. Output: 4K 4096x2160 with film grain, 45-sec"},
        {"level": "expert", "prompt": "3D motion graphics — Rangoli powder spreading. Technique: GPU particle system with physics-based color mixing. Shader: custom GLSL blend modes. Render: 60fps WebGL with interactive mouse tracking + 4K pre-rendered version. Loopable"},
        {"level": "expert", "prompt": "Data visualization — India population density choropleth (10-year time-lapse). Animation: custom per-state easing transitions. Camera: dynamic pan across regions. Tools: d3.js + After Effects. Output: 1920x1080 broadcast-safe with synced lower-third text"},
    ],

    # ─── NEW CATEGORY 5: PHOTOGRAPHY STYLES ──────────────────────────────────
    "photography_styles": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Bright airy portrait. Subject: Indian woman. Lighting: natural window light, soft shadows. Background: white. Aesthetic: clean Instagram style. Camera: shot on iPhone"},
        {"level": "beginner", "prompt": "Golden-hour street photo. Subject: Indian marketplace. Lighting: warm orange tone. Style: candid people, lifestyle feel. Camera: shot on smartphone"},
        {"level": "beginner", "prompt": "Flat lay product photo. Subject: Indian spices in small bowls. Background: warm wood. Lighting: natural light, minimal props. Angle: overhead"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Noir portrait — 1950s Mumbai café. Subject: Indian man. Lighting: single overhead tungsten, deep shadow pools (70% black), wet pavement reflections. Film: Kodak 5219 emulation, 800 ISO grain. Lens: 85mm f/1.4. Palette: desaturated mid-tones, punchy highlights"},
        {"level": "professional", "prompt": "Surreal fine-art portrait. Concept: Indian woman + Ajanta fresco merge with intricate fresco pattern painting on skin. Lighting: soft ethereal. Palette: teal-terracotta-gold. Technique: double-exposure composite. Depth: dreamlike DOF. Format: 4:3 medium-format crop, 8K"},
        {"level": "professional", "prompt": "High-fashion editorial — Indian model in avant-garde silhouette. Setup: stark studio with large-format strobe. Lighting: dramatic deep shadow, negative space. Composition: Vogue India aesthetic. Sensor: Phase One 150MP. Format: 8x10 portrait"},
        {"level": "professional", "prompt": "Documentary street — blue-hour chai stall, Old Delhi. Lighting: available light (fluorescent + fire), authentic gritty. Lens: 35mm f/2.8 wide-angle. Composition: photojournalism with intentional motion blur. Film: Tri-X 400 B&W"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Architectural study — 19th-century Indo-Saracenic railway station. Camera: 4x5 view camera with perspective correction. Exposure: zone system (Zone III-VIII). Print: platinum-palladium emulation. Detail: ultra-sharp corner-to-corner. Composition: architectural symmetry (Ansel Adams). Output: 8K scan"},
        {"level": "expert", "prompt": "Multiple-exposure fine art — Indian classical dance (Bharatanatyam). Technique: 7-layer in-camera exposure with color-channel separation. Effect: motion-spectrum rainbow body trail. Speed: 1/8000s per frame. Style: abstract-expressionist. Sensor: 100MP"},
        {"level": "expert", "prompt": "Computational macro — Indian coin collection. Technique: 200-image focus-stack at 1:1 macro with 0.02mm interval. Processing: Zerene stacker. Detail: infinitely sharp surfaces. Resolution: 500MP effective output. Quality: scientific illustration, museum-archive standard"},
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

