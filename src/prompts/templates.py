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
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Professional Indian woman in formal corporate office wear, standing tall with shoulders back, one hand on desk, head slightly tilted upward showing confidence and eye contact, powerful executive pose, studio lighting, professional headshot aesthetic, 8k quality. Facial feature preservation (face shape, eye shape & color, nose, lips, skin tone, complexion — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, eye shape & color, nose, lips, skin tone, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Beautiful Indian woman in traditional silk saree, standing gracefully with one shoulder forward, hand delicately placed on chest, body angled three-quarters to camera, soft serene expression, elegant sophisticated pose, studio lighting, glamour photography style, 8k quality. Facial feature preservation (face shape, eye shape & color, nose, lips, skin tone, complexion — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, eye shape & color, nose, lips, skin tone, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Young Indian woman in modern fusion wear (traditional meets contemporary), dynamic power pose with one leg forward, arms positioned confidently, modern editorial stance, professional lighting, high fashion magazine aesthetic, contemporary pose, 8k quality. Facial feature preservation (face shape, eye shape & color, nose, lips, skin tone, complexion — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, eye shape & color, nose, lips, skin tone, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian bride in traditional bridal wear (ornate lehenga/saree), seated or standing with regal posture, one hand raised gracefully showing jewelry, dignified royal pose, dramatic warm lighting, wedding photography aesthetic, 8k quality. Facial feature preservation (face shape, eye shape & color, nose, lips, skin tone, complexion — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, eye shape & color, nose, lips, skin tone, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian woman as lifestyle influencer, candid walking pose with natural arm movement, relaxed confident stride, turning slightly toward camera with engaging smile, Instagram-worthy body language, natural lighting, contemporary pose, 8k quality. Facial feature preservation (face shape, eye shape & color, nose, lips, skin tone, complexion — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, eye shape & color, nose, lips, skin tone, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Glamorous Indian woman with theatrical makeup, sitting or reclined in magazine cover pose, one arm extended gracefully, chin slightly raised showing profile and face, dramatic glamorous posture, professional beauty lighting, luxurious aesthetic, 8k quality. Facial feature preservation (face shape, eye shape & color, nose, lips, skin tone, complexion — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, eye shape & color, nose, lips, skin tone, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Fit Indian woman in gym/fitness wear, dynamic athletic pose with one leg extended or lunging position, arms flexed or in action position, powerful energetic posture, motivational lighting, fitness model stance, 8k quality. Facial feature preservation (face shape, eye shape & color, nose, lips, skin tone, complexion — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, eye shape & color, nose, lips, skin tone, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian woman in traditional wedding ceremony ethnic wear, standing with hands in traditional mudra or prayer position, joyful celebratory posture with radiant smile, traditional pose, festive ceremonial lighting, 8k quality. Facial feature preservation (face shape, eye shape & color, nose, lips, skin tone, complexion — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, eye shape & color, nose, lips, skin tone, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Glamorous Indian woman as Bollywood celebrity, dramatic pose leaning against surface, one leg bent, theatrical hand placement, expressive confident posture, dramatic red carpet lighting, cinema-quality stance, 8k quality. Facial feature preservation (face shape, eye shape & color, nose, lips, skin tone, complexion — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, eye shape & color, nose, lips, skin tone, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian woman as travel influencer, adventurous action pose (standing on cliff, hiking stance, or exploration position), looking toward horizon, wanderlust posture, exotic destination background, adventurous body language, 8k quality. Facial feature preservation (face shape, eye shape & color, nose, lips, skin tone, complexion — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, eye shape & color, nose, lips, skin tone, complexion, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
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
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Professional Indian man in formal business suit, standing tall with hands in power position, slight body angle showing confidence, direct eye contact with camera, commanding executive pose, office background, corporate executive aesthetic, professional headshot, 8k quality. Facial feature preservation (face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Handsome Indian man in traditional kurta pajama, standing gracefully with one hand on chest, composed dignified posture, soft focused gaze, elegant sophisticated pose, studio lighting, cultural photography aesthetic, 8k quality. Facial feature preservation (face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Athletic Indian man in gym wear, dynamic power pose with arms flexed, strong confident stance, body positioned to show physique, motivational expression, fitness photography aesthetic, motivational lighting, 8k quality. Facial feature preservation (face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Glamorous Indian man as Bollywood actor, dramatic pose leaning against surface, one hand raised, intense eye contact, theatrical confident posture, dramatic red carpet lighting, cinema-quality photography, celebrity aesthetic, 8k quality. Facial feature preservation (face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Trendy Indian man as lifestyle influencer, relaxed confident standing pose, one hand in pocket, casual cool posture, engaging smile toward camera, natural lighting, Instagram aesthetic, contemporary styling, 8k quality. Facial feature preservation (face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian man in traditional festival wear (sherwani, ethnic), standing regal with hands at sides or gestured gracefully, celebratory joyful posture, warm proud expression, golden warm lighting, festive aesthetic, 8k quality. Facial feature preservation (face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian man as travel influencer, adventurous action pose (standing on mountain, exploring position, or outdoor adventure stance), looking outward or toward horizon, wanderlust posture, exotic location, passport vibes, 8k quality. Facial feature preservation (face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Artistic creative Indian man, sophisticated pose leaning or seated artistically, thoughtful composed expression, creative positioning, artistic background, creative professional pose, cultured aesthetic, 8k quality. Facial feature preservation (face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Luxury lifestyle Indian man, standing confidently in premium designer wear, composed elegant posture, sophisticated expression, high-end background, confident elegant pose, expensive upscale aesthetic, 8k quality. Facial feature preservation (face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Charismatic Indian man for dating profile, warm romantic lighting, relaxed approachable pose with gentle smile, one hand on chest or reaching out, engaging direct eye contact, attractive welcoming aesthetic, 8k quality. Facial feature preservation (face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair — MUST MATCH REFERENCE EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGE. Preserve subject's exact facial features: face shape, jawline, eye shape & color, nose, lips, skin tone, beard/facial hair, facial characteristics. Match 100% exactly. Do NOT vary face. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
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
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian couple in professional pre-wedding photoshoot, bride facing forward with hand on groom's chest, groom standing behind with arms around bride, romantic intimate connection, outdoor garden golden hour lighting, professional photography aesthetic, traditional jewelry, elegant aesthetic, 8k quality. Facial feature preservation for BOTH subjects (individual face shapes, eye shapes & colors, noses, lips, skin tones, complexions — MUST MATCH REFERENCE IMAGES EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGES. Preserve both subjects' exact facial features, individual skin tones, complexions, unique facial characteristics (eyes, nose, lips, face shape) from reference images. Each subject Match 100% exactly. Do NOT vary faces. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian couple on wedding day, bride in bridal lehenga/saree facing slightly left, groom on right looking toward bride, facing each other with joyful expressions, festive joyful pose, wedding ceremony lighting, ceremonial aesthetic, 8k quality. Facial feature preservation for BOTH subjects (individual face shapes, eye shapes & colors, noses, lips, skin tones, complexions — MUST MATCH REFERENCE IMAGES EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGES. Preserve both subjects' exact facial features, individual skin tones, complexions, unique facial characteristics (eyes, nose, lips, face shape) from reference images. Each subject Match 100% exactly. Do NOT vary faces. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Young engaged Indian couple, couple sitting close together facing camera, hands intertwined, romantic elegant pose, studio lighting, professional engagement photography aesthetic, intimate moment, 8k quality. Facial feature preservation for BOTH subjects (individual face shapes, eye shapes & colors, noses, lips, skin tones, complexions — MUST MATCH REFERENCE IMAGES EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGES. Preserve both subjects' exact facial features, individual skin tones, complexions, unique facial characteristics (eyes, nose, lips, face shape) from reference images. Each subject Match 100% exactly. Do NOT vary faces. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian couple celebrating anniversary, both standing facing each other with warm embrace, intimate connection pose, romantic dining setting, candlelight ambiance, celebratory pose, romantic aesthetic, 8k quality. Facial feature preservation for BOTH subjects (individual face shapes, eye shapes & colors, noses, lips, skin tones, complexions — MUST MATCH REFERENCE IMAGES EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGES. Preserve both subjects' exact facial features, individual skin tones, complexions, unique facial characteristics (eyes, nose, lips, face shape) from reference images. Each subject Match 100% exactly. Do NOT vary faces. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian couple on honeymoon vacation, both walking hand in hand toward horizon, relaxed joyful pose, casual vacation wear, exotic tropical background, sunset romantic lighting, wanderlust aesthetic, 8k quality. Facial feature preservation for BOTH subjects (individual face shapes, eye shapes & colors, noses, lips, skin tones, complexions — MUST MATCH REFERENCE IMAGES EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGES. Preserve both subjects' exact facial features, individual skin tones, complexions, unique facial characteristics (eyes, nose, lips, face shape) from reference images. Each subject Match 100% exactly. Do NOT vary faces. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian couple celebrating Holi festival, playfully posing together with colored powder, energetic dynamic pose, colorful traditional festival clothes, playful energetic movement, festive colorful lighting, celebration mood, joyful aesthetic, 8k quality. Facial feature preservation for BOTH subjects (individual face shapes, eye shapes & colors, noses, lips, skin tones, complexions — MUST MATCH REFERENCE IMAGES EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGES. Preserve both subjects' exact facial features, individual skin tones, complexions, unique facial characteristics (eyes, nose, lips, face shape) from reference images. Each subject Match 100% exactly. Do NOT vary faces. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian couple on romantic dinner date, both seated at table leaning toward each other, intimate loving gaze, romantic loving pose, formal elegant wear, intimate restaurant candlelight setting, intimate aesthetic, 8k quality. Facial feature preservation for BOTH subjects (individual face shapes, eye shapes & colors, noses, lips, skin tones, complexions — MUST MATCH REFERENCE IMAGES EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGES. Preserve both subjects' exact facial features, individual skin tones, complexions, unique facial characteristics (eyes, nose, lips, face shape) from reference images. Each subject Match 100% exactly. Do NOT vary faces. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Trendy modern Indian couple as influencers, couple back-to-back posing, both looking toward camera with confident relaxed poses, contemporary stylish wear, Instagram-worthy background, candid confident pose, modern aesthetic, relatable yet stylish, 8k quality. Facial feature preservation for BOTH subjects (individual face shapes, eye shapes & colors, noses, lips, skin tones, complexions — MUST MATCH REFERENCE IMAGES EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGES. Preserve both subjects' exact facial features, individual skin tones, complexions, unique facial characteristics (eyes, nose, lips, face shape) from reference images. Each subject Match 100% exactly. Do NOT vary faces. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Luxury lifestyle Indian couple, couple standing together facing forward, confident elegant posture, premium designer wear, high-end upscale background, sophisticated elegant pose, expensive upscale aesthetic, 8k quality. Facial feature preservation for BOTH subjects (individual face shapes, eye shapes & colors, noses, lips, skin tones, complexions — MUST MATCH REFERENCE IMAGES EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGES. Preserve both subjects' exact facial features, individual skin tones, complexions, unique facial characteristics (eyes, nose, lips, face shape) from reference images. Each subject Match 100% exactly. Do NOT vary faces. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
        "EXACT FACE MATCH + IDENTITY PRESERVATION: Indian couple in traditional wedding ceremony, bride and groom facing each other in sacred ritual pose, bride in full bridal saree, groom in traditional sherwani, temple ceremonial setting, sacred moment connection, cultural photography aesthetic, 8k quality. Facial feature preservation for BOTH subjects (individual face shapes, eye shapes & colors, noses, lips, skin tones, complexions — MUST MATCH REFERENCE IMAGES EXACTLY). Identity-locked rendering. Do NOT vary facial features. — USE FACE_ID FROM REFERENCE IMAGES. Preserve both subjects' exact facial features, individual skin tones, complexions, unique facial characteristics (eyes, nose, lips, face shape) from reference images. Each subject Match 100% exactly. Do NOT vary faces. Apply identity-consistency technique. Keep original facial anatomy intact. Maintain exact facial geometry - No face modifications - Identity-locked to reference - Facial structure immutable.",
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
        {"level": "professional", "prompt": "Editorial illustration for tech article: Indian woman coder surrounded by floating holographic UI elements, isometric perspective, vibrant jewel-tone palette, textured grain overlay, Procreate digital painting style, 2400x1600px editorial format"},
        {"level": "professional", "prompt": "Children's book illustration: Indian village festival at night, Diwali lamps reflected in river, warm painterly gouache style, soft lighting, rich storytelling composition, 3000x2000px, 300dpi"},
        {"level": "professional", "prompt": "Concept art for mobile game: Indian mythology character — Arjuna as modern archer hero, dynamic action pose, detailed armour inspired by Mahabharata, painterly rendering, dramatic rim-lighting, cinematic composition, 2K square format"},
        {"level": "professional", "prompt": "Infographic illustration: Indian spice market, 8 spice icons with hand-drawn linework, watercolour texture fill, editorial serif labels, warm earthy palette, A3 print layout"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Hyper-detailed surrealist digital painting: Indian classical dancer transforming into cosmic deity, body formed from thousands of micro-marigolds, skin tone shifts from warm terracotta to celestial indigo, each petal individually rendered, Beeple-inspired grandiosity, 8K UHD, ZBrush-level surface detail simulation in 2D paint"},
        {"level": "expert", "prompt": "Graphic novel cover: dystopian Mumbai 2087, neo-noir palette (acid yellow / noir black / rust orange), ink-wash + digital hybrid technique, layered atmospheric haze, crowd of diverse cyberpunk Indian characters in foreground, monumental broken architecture mid-ground, blood-red sky, Frank Miller composition influence, 210x297mm A4 bleed"},
        {"level": "expert", "prompt": "Generative art-inspired illustration: algorithmically composed mandala built from Tamil Kolam patterns, parametric symmetry, 256-colour gradient palette cycling through HSL spectrum, ultra-fine linework at 0.1pt, suitable for large-format canvas print 120x120cm at 300dpi"},
    ],

    # ─── NEW CATEGORY 4: ANIMATION & MOTION GRAPHICS ─────────────────────────
    "animation_motion": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Simple logo reveal animation, fade-in with slight scale, 2 seconds, clean white background, ease-in-out timing, exported as GIF and MP4"},
        {"level": "beginner", "prompt": "Instagram story animated text, bold headline types on screen word by word, colourful background, 5 seconds loop, After Effects template style"},
        {"level": "beginner", "prompt": "Basic loading spinner animation, circular progress ring in brand colour, smooth 1-second loop, transparent background, Lottie JSON format"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Brand intro sting: 3-second logo animation for Indian tech startup, particle swarm assembles into wordmark, deep blue background, subtle lens flare, professional audio sync (logo hit at beat), After Effects, 1920x1080 ProRes export"},
        {"level": "professional", "prompt": "Animated explainer video segment: 30-second 2D motion graphic explaining UPI payment flow, flat characters, smooth transitions, kinetic typography, royalty-free upbeat track, Indian market context, 1080x1920 vertical + 1920x1080 horizontal dual export"},
        {"level": "professional", "prompt": "Social media animated carousel: 5-slide product launch sequence, consistent motion language (slide-in left, scale pop), brand colour palette, auto-advancing GIF + MP4 versions, 1080x1080 square format, 24fps"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Cinematic title sequence for Indian web series: hand-drawn frame-by-frame animation of mythological scenes morphing into modern urban setting, 12fps artistic stagger, traditional miniature painting texture, orchestral + electronic hybrid score sync, 4K 4096x2160, film grain overlay, 45-second sequence"},
        {"level": "expert", "prompt": "Real-time 3D motion graphics: GPU particle system simulating Rangoli powder spreading, physics-based colour mixing simulation, GLSL shader custom colour blend modes, 60fps WebGL render, interactive mouse-tracking version + pre-rendered 4K social version, seamlessly loopable"},
        {"level": "expert", "prompt": "Data visualisation animation: India population density morphing choropleth, 10-year time-lapse, custom easing per state transition, camera pan system across geographic regions, d3.js render pipeline + After Effects polish pass, 1920x1080 broadcast-safe, lower-third annotations synced to keyframes"},
    ],

    # ─── NEW CATEGORY 5: PHOTOGRAPHY STYLES ──────────────────────────────────
    "photography_styles": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Bright and airy portrait, Indian woman, natural window light, white background, soft shadows, clean Instagram aesthetic, shot on iPhone"},
        {"level": "beginner", "prompt": "Warm golden-hour street photo, Indian marketplace, orange tone, candid people, shot on smartphone, lifestyle feel"},
        {"level": "beginner", "prompt": "Flat lay product photo, Indian spices in small bowls, warm wood background, natural light, minimal props, overhead angle"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Cinematic noir portrait: Indian man in dimly lit 1950s Mumbai café setting, single overhead tungsten light, deep shadow pools (70% black), wet-pavement reflections, Kodak 5219 film emulation, 85mm f/1.4 perspective, grain 800 ISO, desaturated mid-tones, punchy highlights"},
        {"level": "professional", "prompt": "Surreal fine-art portrait: Indian woman merging with ancient Ajanta cave fresco, skin painted with intricate fresco patterns, soft ethereal lighting, teal-terracotta-gold palette, double-exposure composite, dreamlike depth-of-field, medium-format aesthetic 4:3 crop, 8K"},
        {"level": "professional", "prompt": "High-fashion editorial: Indian model in avant-garde silhouette wear, stark studio setup, large-format strobe with sharp octabox, dramatic deep shadow, editorial negative space, Vogue India aesthetic, Phase One 150MP quality, 8x10 portrait orientation"},
        {"level": "professional", "prompt": "Documentary street photography: blue-hour chai stall in Old Delhi, available light (fluorescent + fire), authentic gritty textures, 35mm f/2.8 wide angle, photojournalism composition, intentional motion blur on vendor hands, Tri-X 400 black-and-white conversion"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Large-format architectural study: 19th-century Indo-Saracenic railway station, 4x5 view camera perspective correction, zone system exposure (Zone III shadows to Zone VIII highlights), platinum-palladium print emulation, ultra-sharp detail from corner to corner, architectural symmetry composition, pre-visualised as Ansel Adams would, 8K scan"},
        {"level": "expert", "prompt": "Experimental multiple-exposure fine art: 7-layer in-camera multiple exposure of Indian classical dance (Bharatanatyam) sequence, intentional colour-channel separation between exposures, resulting in motion-spectrum rainbow body trail, 1/8000s freeze per frame, combined into single raw file, abstract-expressionist final image, 100MP sensor"},
        {"level": "expert", "prompt": "Computational photography composite: 200-image focus-stack macro of Indian coin collection, 1:1 macro lens, 0.02mm focus step interval, zerene stacker processed, every surface detail rendered infinitely sharp, final 500MP effective resolution image, scientific illustration quality, museum-archive standard"},
    ],

    # ─── NEW CATEGORY 6: PRINT DESIGN ────────────────────────────────────────
    "print_design": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "Simple A5 flyer for Indian restaurant, food photo centre, name at top, address at bottom, warm colours, easy to read, print-ready"},
        {"level": "beginner", "prompt": "Basic event poster for Navratri festival, large title text, date and venue, decorative border, saffron and red colours, A4 size"},
        {"level": "beginner", "prompt": "Simple business card, name and contact details, minimal design, white background, brand colour accent stripe, 90x55mm standard size"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Luxury wedding invitation suite: laser-cut gate-fold card, deep burgundy + gold foil letterpress typography, watercolour floral Indian motifs, RSVP card + inner envelope, 5x7 inch 400gsm paper simulation, 300dpi CMYK print-ready with 3mm bleed and crop marks"},
        {"level": "professional", "prompt": "Magazine cover design — Indian fashion monthly: full-bleed editorial portrait, masthead in custom display type, cover lines in hierarchy (kicker / headline / deck), barcode + price placement, newsstand-optimised contrast, A4 bleed 216x303mm, 300dpi, ISO Coated v2 colour profile"},
        {"level": "professional", "prompt": "Corporate annual report spread: infographic-led double-page layout, financial data visualised as elegant charts, brand typographic system, photography + illustration mix, 12-column grid, A4 landscape, print-ready InDesign-style layout, 4mm bleed, Pantone spot colour"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Museum exhibition catalogue: 128-page art book design, Swiss grid system, Futura + Caslon type pairing, full-bleed full-colour artwork reproductions opposite scholarly text pages, running heads, footnotes, index, bibliography, perfect-bound 230x280mm, ICC-profiled FOGRA51 pre-press, ISBN barcode placement"},
        {"level": "expert", "prompt": "Artisanal product packaging system: handmade paper box for premium Indian tea, custom letterpress label with heritage illustration, deboss lid pattern, tissue wrap with spot UV brand mark, unboxing sequence design, eco material callouts, regulatory text hierarchy, dieline for corrugated insert, full print production spec sheet"},
    ],

    # ─── NEW CATEGORY 7: 3D PRODUCT DESIGN ───────────────────────────────────
    "product_3d": [
        # --- BEGINNER ---
        {"level": "beginner", "prompt": "3D product mockup of smartphone app on iPhone, clean studio background, soft shadows, one light source, realistic render, white backdrop"},
        {"level": "beginner", "prompt": "Simple 3D render of perfume bottle, glass material, white background, soft studio lighting, product photography look"},
        {"level": "beginner", "prompt": "3D food product visualisation, Indian snack box packaging, flat lay angle, warm lighting, realistic shadows, e-commerce style"},
        # --- PROFESSIONAL ---
        {"level": "professional", "prompt": "Hero product 3D render: premium skincare serum bottle, borosilicate glass shader, gold metallic dropper cap, caustic light refractions on marble surface, 3-point studio lighting rig, photorealistic PBR materials, 4K render, white + soft warm ambient, Blender Cycles or Cinema 4D Octane"},
        {"level": "professional", "prompt": "Architectural product visualisation: Indian-designed modular furniture in contemporary apartment, natural oak veneer + matte black metal materials, HDRI morning light through floor-to-ceiling window, subsurface scatter on fabric cushions, depth-of-field blur, 4K interior render, ArchViz quality"},
        {"level": "professional", "prompt": "Electronic product launch render: true wireless earbuds in charging case, polished gloss + soft-touch matte mixed materials, studio 3-point key/fill/rim lighting, clean floating product hero shot, dark gradient background with subtle ambient occlusion, Keyshot photorealistic quality, 6K output"},
        # --- EXPERT ---
        {"level": "expert", "prompt": "Hyper-real luxury watch 3D visualisation: Swiss automatic movement partially visible through sapphire caseback, 18k gold case, guilloché dial hand-engraving simulation, bracelet micro-scratches via displacement map, HDRI gem studio lighting, spectral caustics for diamond indices, 16K render, sub-millimetre surface detail, CGI-to-photo indistinguishable"},
        {"level": "expert", "prompt": "Real-time 3D vehicle concept: electric auto-rickshaw redesign for 2040 India, parametric surface modelling, iridescent paint shader with flake simulation, neon underglow, physically accurate headlight IES profiles, real-time ray tracing in Unreal Engine 5 Lumen, cinematic camera rig, 4K 60fps interactive walkthrough + pre-rendered beauty shots"},
    ],
}

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

