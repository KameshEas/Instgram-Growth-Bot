"""Professional Prompt Structure: 12-Component Framework
Implements the professional human image generation structure with embedded best practices.

Structure: [Subject] + [Face Details] + [Hair] + [Expression] + [Clothing] 
         + [Pose] + [Environment] + [Lighting] + [Mood] + [Camera Style] 
         + [Color Palette] + [Quality Keywords]

Professional Secrets Embedded:
- Cinematic lighting techniques
- Realistic skin textures (especially for portraits)
- Emotional expression guidance
- Strong color grading specifications
- Professional camera language (lens types, angles, depth of field)
- Storytelling atmosphere
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
import json
import logging
import re

logger = logging.getLogger(__name__)

# ============================================================================
# NA COMPONENT STANDARDIZATION (Fix C1 & M5)
# ============================================================================
# Single source of truth for N/A marker detection
NA_MARKERS = {
    # Complete list of valid N/A patterns to avoid brittle string matching
    "not_applicable_skip_product": "N/A - skip for product designs unless featuring people",
    "not_applicable_skip_product_simple": "N/A - skip for product designs",
    "not_applicable_skip_modeled": "N/A - skip unless featuring modeled on person",
    "not_applicable_portrait_conditional": "N/A unless featuring portrait elements - if so, use portrait_transformation guidelines",
    "not_applicable_portrait_simple": "N/A unless featuring portrait elements",
    "not_applicable_design": "N/A - design focus",
    "not_applicable_interface": "N/A - interface focus",
    "not_applicable_product": "N/A - product focus",
}

# M5 FIX: Consistent regex pattern for N/A detection
# Matches any string starting with "N/A" followed by optional dash and context
NA_PATTERN = re.compile(r"^N/A\s*(-|unless|:)?", re.IGNORECASE)

def is_component_na(component_data: Any) -> bool:
    """Check if a component is marked as N/A (not applicable for this category).
    M5 FIX: Use consistent regex pattern instead of brittle startswith check.
    
    Args:
        component_data: The component data to check
        
    Returns:
        True if component is N/A, False otherwise
    """
    if isinstance(component_data, str):
        # Check against known N/A markers first (whitelist)
        if component_data in NA_MARKERS.values():
            return True
        # Then check with regex for any other N/A patterns (defensive)
        return bool(NA_PATTERN.match(component_data))
    return False


# ============================================================================
# COMPONENT ORDER (M1 FIX: Single Source of Truth)
# ============================================================================
# Professional 12-component framework in assembly order
# Used by: build_professional_prompt(), professional_prompt_enhancer.py, promptBuilder.js
COMPONENT_ORDER = [
    'subject',           # Who is being depicted
    'face_details',      # Facial characteristics and texture
    'hair',              # Hair styling and appearance
    'expression',        # Facial expression and emotion
    'clothing',          # What subject is wearing
    'pose',              # Body positioning and posture
    'environment',       # Background and setting
    'lighting',          # Lighting setup and quality
    'mood',              # Overall atmosphere and feeling
    'camera_style',      # Camera technique and perspective
    'color_palette',     # Color grading and tone
    'quality_keywords'   # Resolution and quality specifications
]


@dataclass
class PrompComponentData:
    """Structure for a single prompt component"""
    subject: str
    face_details: str
    hair: str
    expression: str
    clothing: str
    pose: str
    environment: str
    lighting: str
    mood: str
    camera_style: str
    color_palette: str
    quality_keywords: str
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for easy access"""
        return asdict(self)


# ============================================================================
# COMPONENT TEMPLATES BY CATEGORY
# ============================================================================
# M2 FIX: Component Typing Standardization Documentation
#
# STANDARD FORMAT: All components should be dict with "base" key for default options
#   "component_name": {
#       "base": [list of options],  # Always provide "base" key
#       "subcategory": [list of options],  # Optional additional subcategories
#   }
#
# LEGACY FORMAT (still supported for backward compatibility):
#   "component_name": [list of options]  # Direct array, no dict wrapper
#
# HANDLING:
#   - get_component_template() returns both formats transparently
#   - select_component() handles both array and string inputs
#   - New categories should use dict format; existing categories maintain current format
#   - Use normalize_component_template() to convert legacy to standard format
#
# EXAMPLES:
#   Dict format: "lighting": {"base": [...], "cinematic": [...]}
#   Array format: "hair": [...]
#   Both handled by existing code through isinstance() checks

COMPONENT_TEMPLATES = {
    # -----------------------------------------------------------------------
    # PORTRAIT TRANSFORMATION CATEGORY (women_transform, men_transform, etc.)
    # -----------------------------------------------------------------------
    "portrait_transformation": {
        "subject": {
            "women": [
                "A stunning woman with striking features, quiet luxury presence",
                "An elegant woman with captivating presence, editorial grace",
                "A beautiful professional woman, refined confidence evident",
                "A radiant woman with confident energy, timeless sophistication",
            ],
            "men": [
                "A handsome man with strong features, sculpted magazine aesthetic",
                "An elegant man with commanding presence, executive refined energy",
                "A striking professional man, bespoke tailored confidence",
                "A confident man with magnetic energy, artisanal authenticity",
            ],
            "couple": [
                "A beautiful couple with complementary features, curated chemistry",
                "An elegant pair with striking presence, editorial moment captured",
                "A couple radiating chemistry and connection, tactile authenticity evident",
            ]
        },
        "face_details": {
            # Professional Secret: Realistic skin textures with emotional resonance + luxury perception
            "base": [
                "natural skin texture with subtle imperfections (lived-in luxury), defined sculpted cheekbones, expressive eyes with depth",
                "realistic complexion showing character and refinement, strong bone structure with precision, piercing gaze with emotional intelligence",
                "luminous complexion with natural contours and micro-texture detail, refined features suggesting heritage, intense eyes with narrative depth",
                "porcelain-like skin with dimensional depth and tactile texture, sculpted features with architectural precision, soulful expression with confidence",
            ],
            "high_quality": "porcelain skin with realistic micro-texture detail (hyper-refined craftsmanship), perfect bone structure without digital artificiality, eyes with natural catchlights and soul-deep resonance"
        },
        "hair": [
            "sleek professionally styled hair with volume, movement and refined texture detail",
            "flowing hair with natural shine, dimensional color depth, tactile movement",
            "meticulously groomed hair with perfect styling, precision grooming detail, bespoke arrangement",
            "luxurious hair with rich color depth, artisanal texture (lived-in elegance), premium styling presence",
            "elegantly arranged hair with curated movement, architectural volume, shine suggesting premium care",
        ],
        "expression": {
            # Professional Secret: Emotional expression guidance for storytelling + quiet luxury confidence
            "natural": [
                "genuine subtle smile with relaxed jaw showing authenticity, confident composed demeanor (editorial sophistication)",
                "thoughtful expression with depth in eyes, serene confidence suggesting narrative intelligence",
                "warm genuine smile reaching the eyes with natural crinkle (tactile authenticity), approachable refinement",
                "composed dignified expression with quiet confidence (luxury restraint), serene presence",
                "radiant authentic joy with natural eye crinkle and imperfect beauty, luminous warmth",
            ],
            "emotional": [
                "passionate intensity in gaze, controlled emotional depth with cinematic quality",
                "vulnerable authentic emotion balanced with quiet confidence, lived-in sincerity",
                "contemplative depth with emotional resonance, introspective narrative power",
                "playful confidence with sparkling eyes, curated spontaneity",
                "mysterious allure with engaging presence, bespoke enigmatic beauty",
            ]
        },
        "clothing": [
            "immaculate tailored professional blazer in complementary color, brushed fabric texture with precise seaming detail",
            "elegant designer gown with sophisticated silhouette, luxurious material draping (silk, cashmere, linen blend) with subtle sheen",
            "refined luxury fashion piece with impeccable tailoring, bespoke construction detail, architectural line work",
            "high-end designer outfit with premium fabric appearance (Italian leather, brushed wool, smoked silk), material contrast visible",
            "bespoke fashion statement with perfect fit and styling, craftsmanship detail evident (stitching, seaming, material layering)",
        ],
        "pose": [
            "confident upright posture with squared shoulders, slight head tilt showing architectural precision",
            "elegant seated position with perfect spinal alignment, relaxed arms with refined hand positioning",
            "dynamic three-quarter turn pose with engaged posture, monumental proportional confidence",
            "refined standing pose with weight balanced gracefully, expressive hand placement showing refinement detail",
            "poised position with natural grace and presence, curated spontaneity suggesting confidence",
        ],
        "environment": [
            "minimalist studio setting with neutral backdrop, negative space strategically composed, breathing room evident",
            "luxury venue with refined background elements (travertine surfaces, brushed brass accents, warm wood), material contrast visible",
            "contemporary professional space with subtle architectural elements (tall ceilings, clean lines, monolithic forms)",
            "elegant interior with tasteful background blur, sophisticated layering suggesting gallery-inspired setting",
            "sophisticated environment with neutral but engaging backdrop, intentional emptiness as design element",
        ],
        "lighting": {
            # Professional Secret: Cinematic intentional lighting showing restraint and control
            "base": "professional three-point lighting with soft key light from 45 degrees creating dimensional modeling, rim light subtly separating subject with warmth, fill light at 50% showing control and sophistication",
            "cinematic": "cinematic studio lighting with directional soft key light creating professional dimension, subtle warm rim light with premium color grading, volumetric light suggesting editorial campaign aesthetic",
            "portrait": "flattering editorial portrait lighting with precision placement, soft diffused daylight quality catching planes with architectural precision, golden-hour highlights with controlled warmth",
            "glamour": "sophisticated glamour lighting showing restraint: soft key + fill + gentle rim, controlled shadows emphasizing bone structure without harshness, luminous quality suggesting luxury",
        },
        "mood": [
            "quiet confidence and editorial poise radiating from controlled presence",
            "sophisticated elegance with refined energy, luxury understatement evident",
            "professional authority balanced with approachability, bespoke confidence",
            "serene composure with magnetic appeal, curated stillness",
            "passionate intensity with controlled emotional depth, artisanal authenticity",
        ],
        "camera_style": {
            # Professional Secret: Specific premium camera equipment language
            "standard": "shot on Hasselblad X2D, 50mm lens, f/2.8 aperture creating flattering subject separation with natural bokeh, shallow depth of field isolating subject beautifully",
            "glamour": "85mm portrait lens (Zeiss Milvus), f/1.4 aperture, extreme subject isolation with creamy premium background bokeh, editorial photography aesthetic",
            "fashion": "professional 70mm equivalent (medium-format), f/2.0 aperture, dramatic perspective with elongated features flattery used in luxury fashion campaigns",
            "editorial": "35mm lens on medium-format body, f/2.5 aperture, slightly wider environmental context capturing luxury hotel campaign aesthetic while maintaining sharp subject focus",
        },
        "color_palette": {
            # Professional Secret: Restrained luxury color grading showing discipline
            "warm": "restrained warm tones with golden-hour color grading (luxury restraint), warm highlights balanced with cool sophisticated shadows, slight warm cast suggesting premium film",
            "cool": "cool sophisticated tones with controlled cyan-blue shadows, warm skin tones preserved, professional restrained color grading showing editorial discipline",
            "neutral_luxe": "neutral professional tones (charcoal + ivory palette) with lifted shadows, controlled contrast (muted palette), premium color grading suggesting quiet luxury",
            "vibrant": "saturated but controlled colors with editorial color grading restraint, strategic high-contrast elements balanced with breathing room",
        },
        "quality_keywords": {
            "base": "8k resolution, ultra high definition, professional photography, highly detailed, sharp focus, editorial campaign aesthetic",
            "full": "8k resolution, ultra high definition, professional photography, highly detailed, sharp focus, masterpiece, award-winning editorial quality, cinematic premium lighting, professional color graded, volumetric atmospheric light, photorealistic with tactile imperfections, studio quality, pristine production, trending on vogue british-vogue editorial",
        }
    },
    
    # -----------------------------------------------------------------------
    # GIFT DESIGN CATEGORY (design_gifts)
    # -----------------------------------------------------------------------
    "design_gifts": {
        "subject": [
            "A personalized gift design concept",
            "A custom branded merchandise piece",
            "A thoughtfully designed gift product",
            "A premium personalized gift item",
            "An elegantly designed custom product",
        ],
        "face_details": "N/A - skip for product designs unless featuring people",
        "hair": "N/A - skip for product designs",
        "expression": "N/A - skip for product designs unless featuring people",
        "clothing": "N/A - skip unless featuring modeled on person",
        "pose": "centered professional product placement, elevated slightly for visual interest, angled to show design clarity",
        "environment": {
            "flat_lay": "clean flat lay composition on premium backdrop, product front-and-center, professional staging",
            "lifestyle": "lifestyle context showing product in use, surrounded by complementary objects, story-telling setup",
            "product_focus": "isolated professional product shot with subtle shadow, emphasis on design detail and color accuracy",
            "premium": "luxury product presentation on premium surface, soft background, professional product photography style",
        },
        "lighting": {
            # Professional Secret: Product lighting for texture showcase
            "base": "professional product lighting with main light from 45 degrees, soft fill light, gentle rim light for edge definition",
            "texture": "directional lighting highlighting product texture and material quality, specular highlights showing surface properties",
            "luxury": "sophisticated lighting with warm fill, subtle dramatic shadows, highlighting premium materials and craftsmanship",
            "flat": "even soft lighting minimizing shadows, consistent color reproduction, accurate product colors",
        },
        "mood": [
            "premium quality and luxury aesthetic",
            "celebratory personal gift feeling",
            "professional refined product presentation",
            "creative unique design expression",
            "warm emotional connection and care",
        ],
        "camera_style": {
            "product_standard": "macro-style 90mm equivalent, f/2.8 aperture, product-focused photography",
            "lifestyle": "50mm equivalent, f/2.0 aperture, environmental context with product as focal point",
            "detail": "macro photography, extreme close-up, texture and material detail visible",
        },
        "color_palette": {
            "vibrant": "bold saturated colors with high contrast, color-graded to product specifications, print-ready color accuracy",
            "premium": "rich sophisticated colors, controlled contrast, professional color management, brand color accuracy",
            "natural": "warm natural tones, earthy color palette, organic aesthetic",
        },
        "quality_keywords": {
            "base": "professional product photography, high definition, sharp focus, detailed textures",
            "full": "professional product photography, high definition, sharp focus, detailed textures, pristine condition, studio quality, professional color grading, product-ready, e-commerce photography, merchandize photography",
        }
    },
    
    # -----------------------------------------------------------------------
    # PREMIUM POSTER DESIGN CATEGORY (design_posters)
    # Premium Design Formula: Minimal Luxury + Cinematic Lighting + Editorial Typography + 
    # Structured Grid + Controlled Colors + Founder-Led Storytelling + Strategic Negative Space
    # -----------------------------------------------------------------------
    "design_posters": {
        "subject": "Premium poster hero composition: oversized ultra-bold typography dominating visual hierarchy, strategic focal point (cinematic portrait / futuristic UI / luxury product), founder-led creative vision evident",
        "face_details": "N/A unless featuring founder/creative identity portrait - if present, cinematic editorial quality with rim lighting and depth",
        "hair": "N/A unless part of founder portrait identity element",
        "expression": "N/A unless founder portrait - if present, confident visionary calm expression",
        "clothing": "N/A - design composition focus (founder portrait only: premium editorial styling if featured)",
        "pose": {
            "base": [
                "ultra-bold geometric sans-serif typography at 40-60% of poster area, layered composition with depth stacking, precision grid-aligned layout",
                "structured 12-column grid alignment, floating card elements with glassmorphism aesthetic, intentional negative space as luxury element",
                "layered poster structure: oversized words (SYSTEM, FUTURE, BUILD, SCALE, AI, EXPERIENCE) cropped at edges for editorial campaign feel",
                "hero subject dominating foreground, metadata typography floating with architectural precision, depth-created perspective illusion",
            ],
            "advanced": [
                "cinematic hero portrait positioned with rule-of-thirds composition, floating futuristic dashboard panels with soft blur parallax",
                "layered UI interfaces floating with glassmorphism, precision spacing on invisible grid, minimal geometric shapes floating in negative space",
                "founder-led identity integrated subtly: portrait in corner with rim lighting, personal vision energy evident through composition authority",
            ]
        },
        "environment": {
            "base": [
                "matte black luxury minimalism foundation: deep black (#0a0a0a) or soft graphite (#2a2a2a) with subtle depth",
                "warm grey gradient subtle backdrop: imperceptible transitions suggesting dimension without texture",
                "white breathing space strategic placement: negative space as designed luxury element",
            ],
            "cinematic": [
                "atmospheric haze with controlled bloom, soft volumetric depth creating studio-quality air",
                "subtle metallic reflection integration: glossy surfaces catching ethereal light for premium perception",
                "architectural alignment with zero random elements: every shape grid-snapped, every spacing intentional",
            ]
        },
        "lighting": {
            "base": [
                "soft key light on hero subject, professional studio quality without harsh overexposure",
                "rim lighting creating separation and premium three-dimensionality, controlled metallic reflections",
                "strategic bloom on typography for editorial campaign glow, minimal effects showing restraint",
            ],
            "cinematic_premium": [
                "editorial photography lighting: soft key + fill + rim creating dimensional realism",
                "controlled bloom on UI elements: subtle glow suggesting technology without sci-fi overload",
                "shadow sophistication: soft shadows with feathered edges, professional studio rendering",
            ],
            "avoid": "RGB neon cyberpunk, harsh overexposed glow, random particle effects, aggressive sci-fi aesthetics"
        },
        "mood": [
            "calm confidence and precision: visionary future clarity without urgency",
            "premium innovation energy: creative technology studio feeling, not consumer electronics ad",
            "editorial luxury storytelling: global campaign poster aesthetic with founder-led vision",
            "refined professional restraint: sophisticated simplicity showing creative intelligence",
            "aspirational creative intelligence: innovation leadership with personal creative touch",
        ],
        "camera_style": {
            "base": [
                "editorial photography composition: cinematic portrait framing with intentional negative space",
                "85-135mm equivalent focal length feel: subject-focused framing with environmental context",
                "architectural alignment and clean framing: compositional precision suggesting engineering",
            ],
            "premium": [
                "Apple-style whitespace precision: maximum breathing room, minimal visual clutter",
                "fashion editorial composition: high-end photography aesthetic adapted to poster medium",
                "studio lighting setup visible in subtle details: professional production quality apparent",
            ]
        },
        "color_palette": {
            "base": [
                "restrained color restriction: base colors only (deep black, soft white, graphite, silver grey, deep violet)",
                "ONE accent color maximum: burnt orange OR electric blue OR emerald OR crimson OR ice silver (choose single dominant)",
                "limited harmony principle: luxury brands avoid color chaos, precision palette shows sophistication",
            ],
            "premium": [
                "metallic accents subtly integrated: glossy silver or copper catches light without overload",
                "color grading with color story: emotional narrative through sophisticated tonal relationships",
                "zero-vibrant saturation excess: muted sophisticated palette creating high-end perception",
            ]
        },
        "quality_keywords": {
            "base": [
                "premium poster, editorial campaign, luxury design, high definition",
                "architectural precision, structured grid, premium innovation branding, poster excellence",
            ],
            "full": [
                "premium poster design, editorial campaign aesthetic, luxury brand positioning, high definition masterpiece",
                "architectural grid precision, Apple-style whitespace sophistication, creative technology studio branding",
                "founder-led innovation identity, cinematic editorial lighting, professional print-ready quality",
                "award-winning poster composition, trending on behance dribbble, design excellence, premium brand perception",
                "minimal luxury layout, futuristic UI integration, strategic negative space, founder creative vision",
                "calm confidence storytelling, visionary future clarity, creative intelligence positioning, professional restraint",
            ]
        }
    },
    
    # -----------------------------------------------------------------------
    # PRINT COLLATERAL DESIGN CATEGORY (print_design)
    # Print Design Formula: Professional Marketing Layout + Structured Information Hierarchy +
    # Premium Typography + Brand Consistency + Print-Optimized Colors + Founder-Led Voice
    # -----------------------------------------------------------------------
    "print_design": {
        "subject": "Professional print collateral: structured marketing composition with clear hierarchy, brand-consistent layout, founder voice integrated, print-optimized information architecture",
        "face_details": "N/A unless featuring founder/brand identity - if present, professional headshot quality with studio lighting",
        "hair": "N/A unless part of founder brand element - if present, polished professional styling",
        "expression": "N/A unless founder presence - if featured, professional confidence and approachable authority",
        "clothing": "N/A - print design focus (founder only: professional premium styling if featured)",
        "pose": {
            "base": [
                "structured information hierarchy with clear visual flow: headline > subheading > body > CTA positioned on invisible grid",
                "print-optimized layout respecting margins, bleeds, and fold lines",
                "12-column grid alignment with intentional spacing: professional architectural precision in layout",
                "balanced asymmetric arrangement: left-heavy visual weight with breathing room on right suggesting premium",
            ],
            "advanced": [
                "founder-led positioning: creative identity visible in layout choices and typographic voice",
                "multi-fold integration: surface 1 headline > surface 2 detailed narrative > surface 3 call-to-action",
                "layered paper stock visualization: texture suggestions creating perceived premium quality",
            ]
        },
        "environment": {
            "base": [
                "clean white or off-white printing canvas: matte finish luxury perception",
                "subtle paper texture suggestion: linen or laid texture implication without overwhelm",
                "color blocking with strategic background areas: premium branded backgrounds integrated with restraint",
            ],
            "premium": [
                "foil stamp metallic accent areas: glossy gold/silver foil on premium stock",
                "die-cut structural interest: shaped edge or window cutout with precision engineering",
                "print finishing integration: emboss/deboss subtle texture, spot UV gloss on key elements",
            ]
        },
        "lighting": {
            "base": [
                "professional studio lighting if photography included: soft key with professional fill",
                "even non-directional illumination: print-neutral lighting showing product clearly",
            ],
            "premium": [
                "subtle shadow and highlight suggesting depth: three-dimensionality in 2D medium",
                "rim lighting on product elements: luxury product photography aesthetic",
            ]
        },
        "mood": [
            "professional trustworthy confidence: brand authority without aggression",
            "founder-led creative vision: personal brand voice evident in design choices",
            "premium brand positioning: luxury perception through restraint and precision",
            "clear purposeful storytelling: information hierarchy shows design intelligence",
            "memorable brand experience: design sophistication creates lasting impression",
        ],
        "camera_style": {
            "base": [
                "product photography composition: professional product showcase if items featured",
                "editorial layout photography: structured composition respecting print architecture",
            ],
            "premium": [
                "flat lay composition: overhead styled photography for print marketing materials",
                "studio setup visibility: professional production quality apparent in execution",
            ]
        },
        "color_palette": {
            "base": [
                "brand color system restricted: 3-4 primary colors maximum (base + one accent color)",
                "CMYK print-optimized: colors precisely calibrated for print reproduction",
                "white space as color: negative space designed as active compositional element",
            ],
            "premium": [
                "sophisticated muted primary palette: deep brand color + neutral + strategic white",
                "single metallic accent: gold or silver foil on premium stock for luxury perception",
                "zero gradients or trendy color effects: timeless classic palette showing restraint",
            ]
        },
        "quality_keywords": {
            "base": [
                "print design, marketing collateral, professional branding, high definition",
                "print-ready color management, structured hierarchy, premium brand identity",
            ],
            "full": [
                "professional print design, marketing collateral excellence, premium brand presentation",
                "structured information hierarchy, print-optimized color, CMYK perfect reproduction",
                "founder-led brand voice, creative positioning, professional marketing communication",
                "award-winning print design, trending print aesthetic, design excellence in collateral",
                "luxury brand perception through precision, architectural grid layout, professional restraint",
                "premium typography hierarchy, brand-consistent composition, print-ready technical excellence",
                "strategic negative space, founder creative vision, memorable brand experience design",
            ]
        }
    },
    
    # -----------------------------------------------------------------------
    # UI/UX DESIGN CATEGORY (ui_ux_design)
    # -----------------------------------------------------------------------
    "ui_ux_design": {
        "subject": "A professional UI/UX interface design",
        "face_details": "N/A - interface focus",
        "hair": "N/A - interface focus",
        "expression": "N/A - interface focus",
        "clothing": "N/A - interface focus",
        "pose": "centered interface layout with optimal visual hierarchy",
        "environment": "digital environment, contextual UI setting, integrated interface context",
        "lighting": {
            "light_mode": "bright clean lighting, high contrast for readability, professional light mode presentation",
            "dark_mode": "sophisticated dark mode lighting, reduced glare, elegant dark aesthetic",
            "adaptive": "balanced lighting for both themes, accessibility-conscious illumination",
        },
        "mood": [
            "professional intuitive interface clarity",
            "modern sophisticated digital experience",
            "user-friendly accessible design",
            "innovative cutting-edge interface",
            "minimalist elegant simplicity",
        ],
        "camera_style": "UI photography, interface presentation, pixel-perfect composition, screen-optimized framing",
        "color_palette": {
            "modern": "contemporary color scheme with accessibility compliance, WCAG-compliant contrast ratios, modern design language",
            "minimalist": "reduced color palette, whitespace emphasis, focused color accents",
            "brand": "brand-aligned color system, consistent design tokens, professional color management",
        },
        "quality_keywords": {
            "base": "UI design, interface design, high definition, pixel-perfect, professional interface",
            "full": "UI design, interface design, high definition, pixel-perfect, professional interface, trending on dribbble, award-winning UX, design excellence, accessibility-compliant, production-ready",
        }
    },
    
    # -----------------------------------------------------------------------
    # ILLUSTRATION & DIGITAL ART CATEGORY (illustration_art)
    # -----------------------------------------------------------------------
    "illustration_art": {
        "subject": "A striking digital illustration artwork",
        "face_details": {
            "portrait": "expressive illustrated facial features with artistic style, emotion-driven character design, illustrated detail work",
            "stylized": "stylized features with artistic interpretation, character personality emphasis, artistic rendering",
        },
        "hair": "artistically rendered hair with style and movement, illustrated with texture and flow",
        "expression": {
            "character": "expressive character emotion, personality-driven expression, artistic emotion portrayal",
            "dynamic": "dynamic expressive energy, action-oriented character presence",
        },
        "clothing": "artistically designed costume or clothing, character-appropriate styling, illustrated detail",
        "pose": "dynamic compelling pose with artistic movement, character-driven positioning",
        "environment": {
            "contextual": "illustrative environmental setting, artwork-complementary surroundings, artistic background",
            "abstract": "abstract artistic environment, conceptual background, artistic abstraction",
        },
        "lighting": {
            "painted": "painted illustrative lighting, artistic shadow rendering, hand-painted light qualities",
            "dramatic": "dramatic illustrative lighting, stylized shadow work, artistic chiaroscuro",
            "luminous": "luminous artistic lighting, ethereal glow quality, magical light rendering",
        },
        "mood": [
            "artistic expressive creativity",
            "compelling character-driven narrative",
            "imaginative whimsical aesthetic",
            "dramatic emotional storytelling",
            "refined artistic sophistication",
        ],
        "camera_style": "illustration artwork, artistic composition, editorial illustration style",
        "color_palette": {
            "vibrant": "vibrant saturated illustration colors, expressive color choices, bold artistic palette",
            "muted": "sophisticated muted artistic colors, restrained palette, artistic color harmony",
            "moody": "moody atmospheric colors, emotionally-driven color choices, dramatic color story",
        },
        "quality_keywords": {
            "base": "digital illustration, artwork, highly detailed, artistic masterpiece",
            "full": "digital illustration, artwork, highly detailed, artistic masterpiece, trending on artstation, concept art, professional illustration, award-winning digital art, illustration excellence, detailed rendering",
        }
    },
    
    # -----------------------------------------------------------------------
    # GENERAL PHOTOGRAPHY CATEGORY (general_photography, photography_styles)
    # -----------------------------------------------------------------------
    "general_photography": {
        "subject": "Professional photography subject",
        "face_details": "if featuring people: natural skin with professional enhancement, authentic beauty emphasis",
        "hair": "naturally styled professional presentation",
        "expression": "authentic natural expression, photographic presence",
        "clothing": "professionally styled appropriate attire",
        "pose": "natural relaxed pose with photographic presence",
        "environment": {
            "location": "scenic location photography, environmental storytelling, landscape context",
            "studio": "professional studio setting, controlled background, studio lighting context",
            "lifestyle": "lifestyle photography context, authentic life documentation, environmental story",
        },
        "lighting": {
            "natural": "golden hour natural lighting, warm sunlight quality, natural photography lighting",
            "studio": "professional studio lighting, three-point setup, controlled quality",
            "dramatic": "dramatic photographic lighting, artistic shadow work, cinematic effect",
        },
        "mood": [
            "authentic documentary aesthetic",
            "warm inviting photography feeling",
            "professional polished presentation",
            "artistic creative vision",
            "emotional narrative quality",
        ],
        "camera_style": {
            "standard": "professional 35-50mm photography, f/2.0 aperture, natural perspective",
            "portrait": "portrait lens 85-135mm, f/2.8 aperture, subject-focused framing",
            "wide": "wide-angle 24-35mm, f/4.0 aperture, environmental context",
        },
        "color_palette": {
            "natural": "natural color photography palette, warm natural tones, authentic color reproduction",
            "graded": "cinematically color-graded photography, artistic color story, professional grading",
            "film": "film photography aesthetic, vintage color grading, analog warmth",
        },
        "quality_keywords": {
            "base": "professional photography, high definition, sharp focus, naturally detailed",
            "full": "professional photography, high definition, sharp focus, naturally detailed, award-winning photography, masterpiece, trending on 500px, pristine quality, cinematic lighting, professional color grading, editorial quality",
        }
    },
    
    # -----------------------------------------------------------------------
    # 3D PRODUCT CATEGORY (product_3d)
    # -----------------------------------------------------------------------
    "product_3d": {
        "subject": "A professionally rendered 3D product",
        "face_details": "N/A - product focus",
        "hair": "N/A - product focus",
        "expression": "N/A - product focus",
        "clothing": "N/A - product focus",
        "pose": "optimal 3D product angle, turntable or studio positioning, product showcase angle",
        "environment": {
            "studio": "3D studio environment, neutral backdrop, professional product staging",
            "lifestyle": "lifestyle 3D environment, product in context scene, story-telling 3D environment",
            "abstract": "abstract 3D environment, geometric backgrounds, minimalist digital staging",
        },
        "lighting": {
            "studio": "3D studio three-point lighting, professional render quality, perfect specular highlights",
            "dramatic": "dramatic 3D lighting, theatrical shadow rendering, cinematic 3D lighting",
            "photorealistic": "photorealistic 3D lighting, ray-traced rendering, physically-based lighting",
        },
        "mood": [
            "premium 3D product presentation",
            "high-tech cutting-edge rendering",
            "professional commercial quality",
            "innovative product showcase",
            "sleek modern product design",
        ],
        "camera_style": "3D product photography, optimized render camera, professional 3D composition",
        "color_palette": {
            "product_true": "accurate product color representation, 3D texture fidelity, material-accurate colors",
            "dramatic": "dramatic 3D color grading, atmospheric render colors, artistic 3D palette",
            "premium": "premium 3D color rendering, luxury material appearance, high-end render colors",
        },
        "quality_keywords": {
            "base": "3D rendering, product render, high definition, perfect quality",
            "full": "3D rendering, product render, high definition, perfect quality, ray tracing, unreal engine quality, octane render, photorealistic 3D, masterpiece 3D art, professional product rendering",
        }
    },
    
    # -----------------------------------------------------------------------
    # WOMEN TRANSFORMATION CATEGORY (women_transform)
    # H1 FIX: Converted from array to dict format for consistency
    # EXPENSIVE FEEL FRAMEWORK INTEGRATED: Material contrast, controlled lighting, negative space, camera language, color discipline, physical imperfection, editorial references
    # -----------------------------------------------------------------------
    "women_transform": {
        "subject": {
            "base": [
                "Using reference image, transform the subject into the new scenario with quiet luxury authenticity",
                "Based on reference image, reimagine the person in a scene with editorial sophistication",
                "Reference image as base, transform into a curated moment with bespoke composition",
                "Using the person from reference image in a scenario suggesting architectural grace",
            ]
        },
        "face_details": {
            "base": [
                "natural skin texture and appearance with subtle imperfections (lived-in luxury, tactile realism)",
                "realistic complexion and features preserving authentic character, refined bone structure",
                "authentic natural appearance with micro-texture detail, genuine emotional depth visible",
                "genuine skin tones and texture showing character refinement, luminous yet grounded",
            ]
        },
        "hair": {
            "base": [
                "with hair matching reference appearance and length, curated yet effortless styling",
                "hair color and style as in reference with subtle shine suggesting premium care",
                "original hair preserving color and cut with movement and dimensional texture",
                "natural hair texture with scenario styling showing architectural arrangement detail",
            ]
        },
        "expression": {
            "base": [
                "with natural engaging expression showing authentic confidence, editorial presence",
                "showing authentic warm expression with narrative depth, quiet confidence evident",
                "genuine relaxed expression suggesting bespoke authenticity, serene presence",
                "friendly natural demeanor with sophisticated refinement, curated spontaneity",
            ]
        },
        "clothing": {
            "base": [
                "wearing scenario-appropriate outfit reflecting setting with material contrast (brushed fabric + silk, leather + linen blend)",
                "dressed authentically with precision tailoring, texture detail evident, bespoke construction",
                "in styled clothing with hyper-refined detailing (stitching visible, material layering), editorial sophistication",
                "with wardrobe choices matching scene through luxury restraint, monochromatic or single-accent discipline",
            ]
        },
        "pose": {
            "base": [
                "positioned naturally in scene showing monumental architectural grace, intentional spacing",
                "positioned authentically with strategic negative space composition, natural yet composed",
                "naturally engaged with setting through curated spontaneity, gallery-inspired framing",
                "comfortably positioned showing refined presence, elegant asymmetric balance",
            ]
        },
        "environment": {
            "base": [
                "in a beautiful transformation scenario with material texture (travertine, brushed wood, soft fabric) contrasts",
                "within the scenic environment showing intentional empty space (breathing room), architectural minimalism",
                "in the atmospheric setting with controlled lighting suggesting hotel luxury campaign",
                "situated in scenario backdrop featuring tall ceilings, monolithic forms, gallery-inspired proportions",
            ]
        },
        "lighting": {
            "base": [
                "with warm natural lighting showing controlled softness, soft directional daylight from windows",
                "with cinematic atmospheric lighting using soft key + gentle rim, editorial photography quality",
                "with professional scenic lighting suggesting studio setup, intentional shadow play showing restraint",
                "with golden hour lighting quality (warm highlights, cool sophisticated shadows) controlled and composed",
            ]
        },
        "mood": {
            "base": [
                "capturing authentic moment and emotion with quiet confidence, editorial narrative",
                "conveying genuine narrative mood with luxury sophistication, serene presence",
                "reflecting scenario atmosphere with curated authenticity, bespoke narrative feeling",
                "showing genuine emotional resonance with refined restraint, artisanal presence",
            ]
        },
        "camera_style": {
            "base": [
                "shot on medium-format (Hasselblad), 85mm equivalent, f/2.0 aperture, editorial quality composition",
                "cinematic framing with depth and precision, soft grain suggesting premium film aesthetic",
                "professional photography with anamorphic lens quality feel, architectural framing precision",
                "editorial quality composition, 35-50mm luxury hotel campaign aesthetic, shallow depth of field",
            ]
        },
        "color_palette": {
            "base": [
                "with warm color grading and restrained natural tones (charcoal + ivory palette), muted luxury",
                "with cinematic color palette showing discipline, warm highlights balanced with cool shadows",
                "with professional color grading restraint, desaturated luxury tones, sophisticated muted aesthetic",
                "with authentic scenario color treatment using single-accent approach (burnt orange OR electric blue), quiet luxury",
            ]
        },
        "quality_keywords": {
            "base": [
                "high definition, sharp detail, authentic photography, tactile realism with imperfections",
                "masterpiece photography, award-winning quality, editorial luxury campaign feel",
                "professional portrait quality, sophisticated restraint, bespoke artisanal aesthetic",
                "cinematic photography excellence, quiet luxury positioning, refined presence",
            ]
        }
    },
    
    # -----------------------------------------------------------------------
    # MEN TRANSFORMATION CATEGORY (men_transform)
    # H1 FIX: Converted from array to dict format for consistency
    # EXPENSIVE FEEL FRAMEWORK INTEGRATED: Material contrast, controlled lighting, negative space, camera language, color discipline, physical imperfection, editorial references
    # -----------------------------------------------------------------------
    "men_transform": {
        "subject": {
            "base": [
                "Using reference image, transform the subject into the new scenario with quiet luxury authority",
                "Based on reference image, reimagine the person in a scene with premium editorial restraint",
                "Reference image as base, transform into a moment suggesting architectural masculine elegance",
                "Using the person from reference image in a scenario with bespoke professional positioning",
            ]
        },
        "face_details": {
            "base": [
                "natural skin texture and appearance with character lines (lived-in luxury, authentic seasoning)",
                "realistic complexion and features showing refined maturity, strong angular structure",
                "authentic natural appearance with micro-texture depth, confident presence evident",
                "genuine skin tones showing tactile realism, sculpted features suggesting executive refinement",
            ]
        },
        "hair": {
            "base": [
                "with hair and facial hair as in reference showing precision grooming detail",
                "hair cut and beard style matching reference with architectural precision, curated authenticity",
                "original styling with scenario-appropriate grooming showing bespoke attention",
                "natural hair preserving length and facial hair with dimensional texture, lived-in sophistication",
            ]
        },
        "expression": {
            "base": [
                "with confident natural expression showing quiet strength, editorial authority",
                "showing authentic composed demeanor suggesting narrative depth, refined presence",
                "genuine engaging expression with intellectual depth, curated confidence",
                "natural confident presence showing restraint and emotional intelligence, bespoke authority",
            ]
        },
        "clothing": {
            "base": [
                "wearing scenario-appropriate attire with material contrast (brushed wool + silk, leather + linen), texture visible",
                "dressed authentically with architectural tailoring precision, bespoke construction detail evident",
                "in styled clothing with hyper-refined details (stitching visible, seam work), luxury restraint",
                "with wardrobe choices showing monochromatic discipline or single-accent luxury, editorial sophistication",
            ]
        },
        "pose": {
            "base": [
                "positioned naturally showing monumental confidence, architectural grace in spacing",
                "positioned with assured professional presence, gallery-inspired compositional balance",
                "naturally engaged with setting through curated authenticity, refined asymmetric stance",
                "comfortably positioned showing executive presence, intentional spatial arrangement",
            ]
        },
        "environment": {
            "base": [
                "in a compelling transformation scenario featuring material contrasts (travertine + brushed brass, glass + warm wood)",
                "within the scenic environment showing intentional negative space (breathing room), minimalist luxury",
                "in the atmospheric setting with controlled lighting suggesting premium hotel or boutique architecture",
                "situated in scenario backdrop with tall proportions, monolithic forms, gallery-inspired scale",
            ]
        },
        "lighting": {
            "base": [
                "with strong natural lighting using soft directional daylight, controlled golden-hour warmth",
                "with dramatic cinematic lighting (editorial discipline), soft key + subtle rim light, restraint evident",
                "with professional atmospheric lighting suggesting luxury penthouse or boutique setting",
                "with cinematic light quality showing three-dimensionality, moody sophisticated shadow play",
            ]
        },
        "mood": {
            "base": [
                "capturing authentic moment with quiet confidence and editorial presence",
                "conveying genuine narrative authority with luxury sophistication, serene strength",
                "reflecting scenario atmosphere with refined restraint, artisanal masculine energy",
                "showing powerful emotional resonance with intellectual depth, bespoke presence",
            ]
        },
        "camera_style": {
            "base": [
                "shot on medium-format (Hasselblad), 85mm equivalent, f/2.0 aperture, editorial masculinity",
                "cinematic framing with depth and architectural precision, soft grain quality",
                "professional photography using anamorphic lens aesthetic, premium executive portraiture",
                "editorial quality composition, luxury hotel campaign framing, shallow depth of field with character",
            ]
        },
        "color_palette": {
            "base": [
                "with sophisticated color grading and restrained tones (charcoal + ivory + warm grey), muted masculinity",
                "with cinematic color palette showing discipline, warm highlights balanced with cool shadows",
                "with professional color treatment emphasizing tonal minimalism, desaturated luxury",
                "with authentic scenario color tone using single-accent restraint (burnt orange OR slate blue), quiet luxury",
            ]
        },
        "quality_keywords": {
            "base": [
                "high definition, sharp detail, authentic photography, tactile imperfections evident",
                "masterpiece photography, award-winning quality, editorial masculine luxury",
                "professional portrait quality, sophisticated restraint, bespoke executive aesthetic",
                "cinematic photography excellence, quiet luxury positioning, refined authority presence",
            ]
        }
    },
    
    # -----------------------------------------------------------------------
    # COUPLES TRANSFORMATION CATEGORY (couples_transform)
    # H1 FIX: Converted from array to dict format for consistency
    # EXPENSIVE FEEL FRAMEWORK INTEGRATED: Material contrast, controlled lighting, negative space, camera language, color discipline, physical imperfection, editorial references, micro-details
    # -----------------------------------------------------------------------
    "couples_transform": {
        "subject": {
            "base": [
                "Using reference images, transform the couple into a romantic intimate moment with quiet luxury aesthetic",
                "Using reference images, transform the couple into an adventure together with editorial sophistication",
                "Using reference images, capture the couple having joyful connection with bespoke authenticity",
                "Using reference images, transform the couple into a tender moment suggesting luxury hotel campaign",
                "Based on reference images, reimagine the couple in a passionate scenario with architectural grace",
                "Based on reference images, reimagine the couple sharing a quiet intimate moment with curated restraint",
                "Reference images as base, transform the couple into a romantic setting with material elegance",
                "Using both people from reference images in a beautiful couple scenario showing editorial chemistry",
            ]
        },
        "relationship_context": {
            "base": [
                "newlyweds celebrating their wedding with quiet luxury joy, premium brand campaign aesthetic",
                "long-time partners in committed romance, seasoned authenticity with refined connection",
                "childhood sweethearts reconnecting, lived-in chemistry with bespoke nostalgia",
                "adventure partners exploring together with artistic partnership energy, monumental experiences",
                "parents capturing intimate family moment, generational love with editorial grace",
                "friends discovering secret connection, authentic chemistry with surprising depth",
                "professional partners with hidden chemistry, workplace restraint meeting passionate authenticity",
                "distant lovers reunited by chance, editorial moment of recognition and reunion elegance",
            ]
        },
        "face_details": {
            "base": [
                "both with natural skin texture and appearance showing character, lived-in authenticity",
                "with realistic complexion and features for both preserving individual character and refinement",
                "both showing authentic natural appearance with micro-texture detail (tactile realism)",
                "genuine natural appearance for both individuals suggesting emotional depth and narrative",
            ]
        },
        "hair": {
            "base": [
                "with hair matching reference appearance and length for both, curated yet effortless movement",
                "hair color and style as in reference images for both with dimensional texture and shine",
                "original hair preserving length and cut for both with romantic movement suggesting premium care",
                "natural hair texture with scenario styling for both showing precision architectural grooming",
            ]
        },
        "expression": {
            "base": [
                "with natural genuine expressions showing emotional connection, editorial authenticity",
                "showing authentic affection and chemistry with quiet confidence, bespoke intimacy",
                "genuine relaxed expressions between them suggesting narrative depth, curated spontaneity",
                "natural warm interaction between both showing refined intimacy, luxury understatement",
            ]
        },
        "clothing": {
            "base": [
                "wearing scenario-appropriate outfits with complementary material contrast (silk + linen, leather + cashmere)",
                "dressed for the new scenario with coordinated styling showing precision detail and texture visibility",
                "styled appropriately for couple setting with architectural tailoring and bespoke construction evident",
                "in contextual costumes matching scenario with hyper-refined detailing (stitching visible, seaming work)",
            ]
        },
        "pose": {
            "base": [
                "positioned naturally showing couple connection with intentional negative space composition",
                "positioned together in scene authentically with gallery-inspired spatial arrangement",
                "naturally engaged with each other and setting through curated asymmetric balance",
                "comfortably positioned showing relationship with monumental architectural grace and spacing",
            ]
        },
        "environment": {
            "base": [
                "in a beautiful couple transformation scenario featuring material contrasts (travertine + brass, glass + wood)",
                "within the scenic romantic environment showing intentional breathing room and minimal composition",
                "in the atmospheric couple setting with luxury hotel campaign aesthetic and precision lighting",
                "situated in scenario backdrop together with tall proportions, monolithic forms, gallery-inspired scale",
            ]
        },
        "lighting": {
            "base": [
                "with warm romantic lighting flattering both using soft directional daylight, controlled golden-hour warmth",
                "with cinematic atmospheric lighting for couple showing three-dimensionality and editorial restraint",
                "with professional lighting enhancing connection through soft key + gentle rim, sophisticated shadows",
                "with golden intimate lighting quality (warm highlights balanced with cool shadows), volumetric atmosphere",
            ]
        },
        "mood": {
            "base": [
                "capturing authentic couple moment and connection with quiet luxury confidence",
                "conveying genuine relationship and emotion with editorial sophistication and restraint",
                "reflecting the scenario with couple chemistry, bespoke narrative authenticity",
                "showing genuine emotional resonance between them with refined presence and artisanal energy",
            ]
        },
        "camera_style": {
            "base": [
                "shot on medium-format (Hasselblad), 85mm equivalent, f/2.0 aperture, professional couple editorial",
                "cinematic framing showing connection and depth with architectural precision, soft film grain",
                "professional couple photography using anamorphic lens aesthetic, premium editorial quality",
                "editorial quality couple composition, luxury hotel campaign aesthetic, shallow depth of field",
            ]
        },
        "color_palette": {
            "base": [
                "with warm intimate color grading using restrained natural tones (charcoal + ivory palette), muted romance",
                "with cinematic romantic color palette showing discipline, warm highlights balanced with cool sophisticated shadows",
                "with professional balanced color treatment emphasizing desaturated luxury tones and tonal minimalism",
                "with authentic scenario color harmony using single-accent approach (burnt orange OR soft blue), quiet luxury",
            ]
        },
        "quality_keywords": {
            "base": [
                "high definition, sharp detail, authentic couple photography, tactile imperfections evident",
                "masterpiece couple photography, award-winning quality, editorial luxury campaign feel",
                "professional couple portrait quality, sophisticated restraint, bespoke romantic aesthetic",
                "cinematic couple photography excellence, quiet luxury positioning, refined intimate presence",
            ]
        }
    }
}


# ============================================================================
# COMPONENT SELECTOR & BUILDER FUNCTIONS
# ============================================================================

def get_component_template(category: str, component: str, subcategory: Optional[str] = None) -> Union[List[str], str]:
    """
    Retrieve template options for a specific component in a category.
    
    L4 FIX: Added example docstring
    
    Args:
        category: e.g., 'portrait_transformation', 'design_gifts', 'design_posters'
        component: e.g., 'subject', 'face_details', 'mood', 'lighting'
        subcategory: Optional subcategory for more specific options
        
    Returns:
        List of template strings or single string
        
    Example:
        >>> templates = get_component_template('portrait_transformation', 'subject')
        >>> len(templates)  # → 4 (women, men subject options)
        >>> templates = get_component_template('portrait_transformation', 'lighting')
        >>> len(templates)  # → 6 (different lighting techniques)
    """
    if category not in COMPONENT_TEMPLATES:
        return f"Unknown category: {category}"
    
    category_templates = COMPONENT_TEMPLATES[category]
    
    if component not in category_templates:
        return f"Unknown component: {component}"
    
    component_options = category_templates[component]
    
    # Handle dictionary-based components with subcategories
    if isinstance(component_options, dict):
        if subcategory and subcategory in component_options:
            return component_options[subcategory]
        elif "base" in component_options:
            return component_options["base"]
        else:
            # Return first available key
            first_key = next(iter(component_options))
            return component_options[first_key]
    
    return component_options


def select_component(options: Union[List[str], str], preference: Optional[int] = None) -> str:
    """
    Select a single component from available options with bounds checking.
    Logs warnings when indices are out of bounds (Fix C3).
    
    L4 FIX: Added example docstring
    
    Args:
        options: List of component options or single string
        preference: Optional index to select specific option (0-based)
        
    Returns:
        Selected component string
        
    Example:
        >>> subject_options = ["A woman", "A man", "A couple"]
        >>> select_component(subject_options, 1)  # → "A man"
        >>> select_component(subject_options, 0)  # → "A woman"
        >>> select_component("fixed_option")  # → "fixed_option"
    """
    if isinstance(options, str):
        return options
    
    if isinstance(options, list):
        if preference is not None:
            if not (0 <= preference < len(options)):
                # C3: Log when bounds are violated
                logger.warning(
                    f"[BOUNDS ERROR] Component index {preference} out of bounds (0-{len(options)-1}). "
                    f"Using first option instead. This may indicate batch processing issues."
                )
                return options[0]
            return options[preference]
        # Default to first option if no preference
        return options[0]
    
    return str(options)


def normalize_component_template(component: Union[List[str], Dict[str, Any]]) -> Dict[str, Any]:
    """
    M2 FIX: Normalize component templates to standard dict format.
    
    Converts legacy array format to standardized dict format with "base" key.
    Safe to call multiple times (idempotent).
    
    Args:
        component: Component in array format [options] or dict format {"base": [...]}
        
    Returns:
        Standardized dict format: {"base": [options]} or existing dict if already standard
        
    Example:
        normalize_component_template(["hair option 1", "hair option 2"])
        → {"base": ["hair option 1", "hair option 2"]}
        
        normalize_component_template({"base": [...], "editorial": [...]})
        → {"base": [...], "editorial": [...]}  # Already standard, returned as-is
    """
    # Already in dict format
    if isinstance(component, dict):
        # Ensure "base" key exists
        if "base" not in component and len(component) > 0:
            # Move first key's value to "base"
            first_key = next(iter(component))
            component["base"] = component.pop(first_key)
        return component
    
    # Convert array format to dict format
    if isinstance(component, list):
        return {"base": component}
    
    # Single string or other format - wrap in dict
    return {"base": [str(component)]} if component else {"base": []}


def build_professional_prompt(
    category: str,
    components: Dict[str, Any],
    include_quality: bool = True
) -> str:
    """
    Build a professional prompt from structured components.
    
    Args:
        category: Category of prompt (e.g., 'portrait_transformation')
        components: Dictionary with component selections:
            {
                'subject_idx': 0,
                'face_details_type': 'high_quality',
                'hair_idx': 1,
                'expression_type': 'emotional',
                ... etc
            }
        include_quality: Whether to include quality keywords at end
        
    Returns:
        Assembled professional prompt string
    """
    
    # M1 FIX: Use single source of truth for component order
    prompt_parts = []
    
    for component in COMPONENT_ORDER:
        if component == 'quality_keywords' and not include_quality:
            continue
        
        # Skip N/A components (not applicable for this category) - C1: Use standardized detection
        templates = get_component_template(category, component)
        if is_component_na(templates):
            continue
        
        # Select appropriate option
        selection_key = f"{component}_idx"
        subcategory_key = f"{component}_type"
        
        if subcategory_key in components:
            selected = select_component(templates, None)
            if isinstance(templates, dict) and components[subcategory_key] in templates:
                selected = templates[components[subcategory_key]]
                if isinstance(selected, list):
                    idx = components.get(selection_key, 0)
                    # C3: Use select_component for bounds checking instead of silent min()
                    selected = select_component(selected, idx)
        else:
            idx = components.get(selection_key, 0)
            selected = select_component(templates, idx)
        
        if selected and not is_component_na(selected):
            prompt_parts.append(selected)
    
    # Join with natural transitions
    prompt = ", ".join(prompt_parts)
    
    # Add period for sentence completion
    if prompt and not prompt.endswith("."):
        prompt += "."
    
    return prompt


def build_simple_prompt(
    category: str,
    component_selections: Optional[Dict[str, int]] = None
) -> str:
    """
    Build a prompt with smart defaults from components.
    
    Args:
        category: Category of prompt
        component_selections: Optional dict with {component_name: index_choice}
        
    Returns:
        Assembled professional prompt
    """
    if component_selections is None:
        component_selections = {}
    
    # Build components dict with indices
    components = {}
    
    # M1 FIX: Use single source of truth for component order
    for component in COMPONENT_ORDER:
        if component in component_selections:
            components[f"{component}_idx"] = component_selections[component]
        else:
            components[f"{component}_idx"] = 0  # Default to first option
    
    return build_professional_prompt(category, components)


def get_category_info(category: str) -> Dict[str, Any]:
    """
    Get metadata and available options for a category.
    
    Returns:
        Dictionary with category structure info
    """
    if category not in COMPONENT_TEMPLATES:
        return {"error": f"Unknown category: {category}"}
    
    templates = COMPONENT_TEMPLATES[category]
    info = {
        "category": category,
        "components": []
    }
    
    for component_name, component_data in templates.items():
        if isinstance(component_data, list):
            info["components"].append({
                "name": component_name,
                "type": "list",
                "options": component_data,
                "default_count": len(component_data)
            })
        elif isinstance(component_data, dict):
            info["components"].append({
                "name": component_name,
                "type": "dict",
                "subcategories": list(component_data.keys()),
                "options_per_subcategory": {k: len(v) if isinstance(v, list) else 1 for k, v in component_data.items()}
            })
        elif isinstance(component_data, str):
            info["components"].append({
                "name": component_name,
                "type": "text",
                "value": component_data[:100] + "..." if len(str(component_data)) > 100 else component_data
            })
    
    return info


# ============================================================================
# PROFESSIONAL SECRETS - EMBEDDED QUALITY ENHANCEMENTS
# ============================================================================

# C4: Consolidated professional secrets with unified structure
# This matches PROFESSIONAL_SECRETS_KEYWORDS in professional_secrets_validator.py
# M3 FIX: Removed keyword overlaps to ensure unique detection across secrets
PROFESSIONAL_SECRETS_KEYWORDS = {
    "cinematic_lighting": {
        "description": "Advanced lighting techniques for cinematic quality",
        "keywords": [
            # Lighting-specific keywords (removed: cinematic, atmospheric, mood)
            "volumetric", "three-point", "global illumination", "backlighting",
            "rim lighting", "side lighting", "color-graded lighting", "golden hour",
            "dramatic lighting", "light source", "lighting setup", "key light",
            "fill light", "practical light", "diffused light", "hard light"
        ]
    },
    "realistic_skin_textures": {
        "description": "Photorealistic skin rendering with character",
        "keywords": [
            # Skin-specific keywords (removed: natural, authentic - moved to emotional)
            "pores", "micro-texture", "subsurface scattering", "imperfections",
            "skin texture", "realistic skin", "complexion", "skin tones",
            "wrinkles", "freckles", "blemishes", "skin detail", "facial texture",
            "natural appearance", "detailed skin"
        ]
    },
    "emotional_expression": {
        "description": "Capturing genuine emotion and storytelling",
        "keywords": [
            # Emotion-specific keywords (added back: narrative, authentic, genuine, storytelling)
            "authentic", "emotional", "genuine", "expression", "emotion",
            "sentiment", "soulful", "sincere", "tender", "vulnerable", "affection",
            "chemistry", "connection", "sincere expression", "natural expression",
            "authentic emotion", "genuine feeling", "dramatic expression"
        ]
    },
    "color_grading": {
        "description": "Professional color grading for mood and impact",
        "keywords": [
            # Color-specific keywords (removed: atmospheric, cinematic, mood, storytelling)
            "color grading", "color palette", "color harmony", "warm tones",
            "cool tones", "saturation", "contrast", "color treatment", "color tone",
            "hue", "desaturation", "graded", "color correction", "tone mapping",
            "color cast", "color temperature", "color balance"
        ]
    },
    "professional_camera_language": {
        "description": "Professional camera and lens techniques",
        "keywords": [
            # Camera-specific keywords (removed: cinematic)
            "focal length", "aperture", "depth of field", "perspective",
            "composition", "85mm", "135mm", "50mm", "compression", "framing",
            "portrait lens", "telephoto", "wide angle", "photography technique",
            "camera angle", "camera setup", "editorial composition", "f-number"
        ]
    },
    "storytelling_atmosphere": {
        "description": "Creating narrative and mood in imagery",
        "keywords": [
            # Atmosphere-specific keywords (added back: narrative, storytelling - removed: cinematic, atmospheric)
            "narrative", "storytelling", "environment", "environmental context",
            "scenario", "mood", "story", "setting", "backdrop", "environmental storytelling",
            "compelling story", "narrative arc", "contextual environment", "atmospheric depth",
            "world-building", "scene setup", "narrative moment"
        ]
    }
}

# Implementation techniques for detailed enhancement (used by enhancer)
PROFESSIONAL_SECRETS = {
    "cinematic_lighting": {
        "description": "Advanced lighting techniques for cinematic quality",
        "techniques": [
            "Three-point lighting with key light at 45 degrees, fill at 50%, rim light for separation",
            "Volumetric lighting with atmospheric particles and light shafts",
            "Global illumination for realistic indirect light bouncing",
            "Color-graded lighting with warm key and cool shadows",
            "Practical lights integrated into scene for authentic motivation",
        ]
    },
    "realistic_skin_textures": {
        "description": "Techniques for photorealistic skin rendering with character",
        "techniques": [
            "Visible pores and micro-textures without over-processing",
            "Natural skin variation with subtle color shifts",
            "Subsurface scattering for skin luminosity",
            "Imperfections preserved (freckles, natural marks, subtle flaws)",
            "Avoid beautification filters and artificial perfection",
        ]
    },
    "emotional_expression": {
        "description": "Capturing genuine emotion and storytelling",
        "techniques": [
            "Eyes: Natural catchlights, micro-expressions, genuine emotion",
            "Mouth: Authentic smiles or expressions matching emotional state",
            "Posture: Body language supporting emotional narrative",
            "Depth: Soul and personality visible in the frame",
            "Authenticity: Real emotion over posed perfection",
        ]
    },
    "color_grading": {
        "description": "Professional color grading for mood and impact",
        "techniques": [
            "Warm highlight/cool shadow split (classic portrait technique)",
            "Color harmony with limited palette supporting mood",
            "Saturation control: accurate colors with intentional grading",
            "Contrast management: lift shadows for lifted bright image or crushed for drama",
            "Color psychology: greens for growth, golds for luxury, blues for trust/calm",
        ]
    },
    "camera_language": {
        "description": "Professional camera and lens techniques",
        "techniques": [
            "Focal length: 35mm for context, 50mm for natural, 85mm for flattery, 135mm for compression",
            "Aperture: f/2.0-f/2.8 for portrait separation, f/1.4-f/1.8 for extreme isolation",
            "Depth of field: Shallow for subject focus, deeper for environmental context",
            "Perspective: Eye-level neutral, higher for vulnerability, lower for power",
            "Composition: Rule of thirds, leading lines, negative space, framing",
        ]
    },
    "storytelling_atmosphere": {
        "description": "Creating narrative and mood in imagery",
        "techniques": [
            "Environmental context supporting character and story",
            "Time of day and season suggesting narrative",
            "Color palette supporting emotional story",
            "Lighting direction creating visual hierarchy and attention",
            "Composition guiding viewer's eye through the narrative",
        ]
    }
}


if __name__ == "__main__":
    # Test the structure
    print("=== Professional Prompt Structure Test ===\n")
    
    # Test portrait transformation
    print("1. PORTRAIT TRANSFORMATION EXAMPLE:")
    portrait_components = {
        'subject_idx': 0,
        'face_details_type': 'high_quality',
        'hair_idx': 1,
        'expression_type': 'emotional',
        'clothing_idx': 0,
        'pose_idx': 1,
        'environment_idx': 1,
        'lighting_type': 'cinematic',
        'mood_idx': 2,
        'camera_style_type': 'glamour',
        'color_palette_type': 'warm',
        'quality_keywords_type': 'full'
    }
    prompt = build_professional_prompt('portrait_transformation', portrait_components)
    print(prompt)
    print()
    
    # Test design gifts
    print("2. DESIGN GIFTS EXAMPLE:")
    gift_components = {
        'subject_idx': 0,
        'pose_idx': 1,
        'environment_type': 'premium',
        'lighting_type': 'luxury',
        'mood_idx': 1,
        'color_palette_type': 'premium',
        'quality_keywords_type': 'full'
    }
    prompt = build_professional_prompt('design_gifts', gift_components)
    print(prompt)
    print()
    
    # Test category info
    print("3. CATEGORY INFO - portrait_transformation:")
    info = get_category_info('portrait_transformation')
    print(f"Components available: {len(info['components'])}")
    for comp in info['components'][:3]:
        print(f"  - {comp['name']}: {comp['type']}")
