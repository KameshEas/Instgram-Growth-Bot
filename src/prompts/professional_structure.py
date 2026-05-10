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

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import json


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

COMPONENT_TEMPLATES = {
    # -----------------------------------------------------------------------
    # PORTRAIT TRANSFORMATION CATEGORY (women_transform, men_transform, etc.)
    # -----------------------------------------------------------------------
    "portrait_transformation": {
        "subject": {
            "women": [
                "A stunning woman with striking features",
                "An elegant woman with captivating presence",
                "A beautiful professional woman",
                "A radiant woman with confident energy",
            ],
            "men": [
                "A handsome man with strong features",
                "An elegant man with commanding presence",
                "A striking professional man",
                "A confident man with magnetic energy",
            ],
            "couple": [
                "A beautiful couple with complementary features",
                "An elegant pair with striking presence",
                "A couple radiating chemistry and connection",
            ]
        },
        "face_details": {
            # Professional Secret: Realistic skin textures with emotional resonance
            "base": [
                "natural skin texture with subtle imperfections, defined cheekbones, expressive eyes",
                "realistic skin with visible character, strong bone structure, piercing gaze",
                "luminous complexion with natural contours, refined features, intense eyes",
                "porcelain-like skin with depth, sculpted features, soulful expression",
            ],
            "high_quality": "porcelain skin with realistic micro-texture, perfect bone structure without artificiality, eyes with natural catchlights and depth"
        },
        "hair": [
            "sleek professionally styled hair with volume and movement",
            "flowing hair with natural shine and dimension",
            "meticulously groomed hair with perfect styling and texture",
            "luxurious hair with rich color depth and professional styling",
            "elegantly arranged hair with movement and shine",
        ],
        "expression": {
            # Professional Secret: Emotional expression guidance for storytelling
            "natural": [
                "genuine subtle smile with relaxed jaw, confident composed demeanor",
                "thoughtful expression with depth in eyes, serene confidence",
                "warm genuine smile reaching the eyes, approachable warmth",
                "composed dignified expression with quiet confidence",
                "radiant authentic joy with natural eye crinkle",
            ],
            "emotional": [
                "passionate intensity in gaze, controlled emotional depth",
                "vulnerable authentic emotion balanced with confidence",
                "contemplative depth with emotional resonance",
                "playful confidence with sparkling eyes",
                "mysterious allure with engaging presence",
            ]
        },
        "clothing": [
            "immaculate tailored professional blazer in complementary color",
            "elegant designer gown with sophisticated silhouette",
            "refined luxury fashion piece with impeccable tailoring",
            "high-end designer outfit with premium fabric appearance",
            "bespoke fashion statement with perfect fit and styling",
        ],
        "pose": [
            "confident upright posture with squared shoulders, slight head tilt",
            "elegant seated position with perfect spinal alignment, relaxed arms",
            "dynamic three-quarter turn pose with engaged posture",
            "refined standing pose with weight balanced, expressive hand placement",
            "poised position with natural grace and presence",
        ],
        "environment": [
            "minimalist studio setting with neutral backdrop",
            "luxury venue with refined background elements",
            "contemporary professional space with subtle architectural elements",
            "elegant interior with tasteful background blur",
            "sophisticated environment with neutral but engaging backdrop",
        ],
        "lighting": {
            # Professional Secret: Cinematic lighting with color grading
            "base": "professional three-point lighting with key light from 45 degrees, rim light separating subject from background, fill light at 50% key intensity",
            "cinematic": "cinematic studio lighting with soft key light creating dimension, subtle rim light with warm color grading, global illumination effect",
            "portrait": "flattering portrait lighting with golden ratio placement, modeled light catching planes of face, professional color temperature",
            "glamour": "glamorous dramatic lighting with controlled shadows emphasizing bone structure, high-key setup with luminous quality",
        },
        "mood": [
            "confidence and poise radiating from powerful presence",
            "sophisticated elegance with refined energy",
            "professional authority balanced with approachability",
            "serene composure with magnetic appeal",
            "passionate intensity with controlled emotional depth",
        ],
        "camera_style": {
            # Professional Secret: Professional camera language
            "standard": "professional 50mm portrait lens, f/2.8 aperture for flattering subject separation, shallow depth of field isolating subject",
            "glamour": "85mm portrait lens, f/1.4 aperture, extreme subject isolation with creamy background bokeh",
            "fashion": "professional 70mm equivalent, f/2.0 aperture, dramatic perspective with elongated features flattery",
            "editorial": "35mm lens, f/2.5 aperture, slightly wider field capturing environment context while maintaining subject focus",
        },
        "color_palette": {
            # Professional Secret: Strong color grading specifications
            "warm": "rich warm tones with golden hour color grading, warm highlights and cool shadows, slight orange-brown cast in shadows",
            "cool": "cool sophisticated tones with cyan-blue shadows, warm skin highlights, professional cool color grading",
            "neutral_luxe": "neutral professional tones with lifted shadows, controlled contrast, premium color grading",
            "vibrant": "saturated rich colors with dramatic color grading, high contrast between subject and background",
        },
        "quality_keywords": {
            "base": "8k resolution, ultra high definition, professional photography, highly detailed, sharp focus",
            "full": "8k resolution, ultra high definition, professional photography, highly detailed, sharp focus, masterpiece, trending on artstation, award-winning, cinematic lighting, color graded, volumetric lighting, ray tracing, photorealistic, studio quality, pristine condition",
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
    # GRAPHIC DESIGN / POSTER CATEGORY (design_posters)
    # -----------------------------------------------------------------------
    "design_posters": {
        "subject": "A striking graphic design composition",
        "face_details": "N/A unless featuring portrait elements - if so, use portrait_transformation guidelines",
        "hair": "N/A unless featuring portrait elements",
        "expression": "N/A unless featuring portrait elements",
        "clothing": "N/A - design focus",
        "pose": "compositional layout with visual hierarchy, balanced asymmetric arrangement, dynamic negative space",
        "environment": "clean design canvas, integrated background elements, compositional staging",
        "lighting": {
            "base": "even graphic lighting without harsh shadows, emphasis on color vibrancy and clarity",
            "dramatic": "dramatic contrast lighting for visual impact, theatrical shadowing for depth",
            "editorial": "sophisticated lighting treatment with controlled tonal ranges, print-ready lighting",
        },
        "mood": [
            "visually striking and attention-grabbing",
            "professionally composed and intentional",
            "emotionally resonant storytelling",
            "bold confident design energy",
            "refined sophisticated visual appeal",
        ],
        "camera_style": "design composition photography, optimized for print, compositional integrity prioritized",
        "color_palette": {
            "bold": "high contrast color scheme, vibrant saturation, dramatic color relationships, psychological color theory applied",
            "sophisticated": "carefully curated color palette, limited harmonious colors, professional color grading",
            "editorial": "editorial color grading with color story, strategic color emphasis, sophisticated tonal relationships",
        },
        "quality_keywords": {
            "base": "graphic design, high definition, sharp composition, professional design",
            "full": "graphic design, high definition, sharp composition, professional design, trending on behance, award-winning graphic design, pristine quality, design excellence, print-ready, color managed",
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
    # -----------------------------------------------------------------------
    "women_transform": {
        "subject": [
            "Using reference image, transform the subject into the new scenario",
            "Based on reference image, reimagine the person in",
            "Reference image as base, transform into",
            "Using the person from reference image in",
        ],
        "face_details": [
            "natural skin texture and appearance",
            "realistic complexion and features",
            "authentic natural appearance",
            "genuine skin tones and texture",
        ],
        "hair": [
            "with hair matching reference appearance and length",
            "hair color and style as in reference",
            "original hair preserving color and cut",
            "natural hair texture with scenario styling",
        ],
        "expression": [
            "with natural engaging expression",
            "showing authentic warm expression",
            "genuine relaxed expression",
            "friendly natural demeanor",
        ],
        "clothing": [
            "wearing scenario-appropriate outfit reflecting the setting",
            "dressed authentically for the transformation context",
            "in styled clothing suited to the scenario",
            "with wardrobe choices matching the scene",
        ],
        "pose": [
            "positioned naturally in the scene",
            "positioned authentically in the environment",
            "naturally engaged with the setting",
            "comfortably positioned in the scenario",
        ],
        "environment": [
            "in a beautiful transformation scenario",
            "within the scenic environment",
            "in the atmospheric setting",
            "situated in the scenario backdrop",
        ],
        "lighting": [
            "with warm natural lighting",
            "with cinematic atmospheric lighting",
            "with professional scenic lighting",
            "with golden hour lighting quality",
        ],
        "mood": [
            "capturing authentic moment and emotion",
            "conveying genuine narrative mood",
            "reflecting the scenario atmosphere",
            "showing genuine emotional resonance",
        ],
        "camera_style": [
            "professional portrait composition, 85mm focal length feel",
            "cinematic framing with depth",
            "professional photography aesthetic",
            "editorial quality composition",
        ],
        "color_palette": [
            "with warm color grading and natural tones",
            "with cinematic color palette",
            "with professional color grading",
            "with authentic scenario color treatment",
        ],
        "quality_keywords": [
            "high definition, sharp detail, authentic photography",
            "masterpiece photography, award-winning quality",
            "professional portrait quality",
            "cinematic photography excellence",
        ]
    },
    
    # -----------------------------------------------------------------------
    # MEN TRANSFORMATION CATEGORY (men_transform)
    # -----------------------------------------------------------------------
    "men_transform": {
        "subject": [
            "Using reference image, transform the subject into the new scenario",
            "Based on reference image, reimagine the person in",
            "Reference image as base, transform into",
            "Using the person from reference image in",
        ],
        "face_details": [
            "natural skin texture and appearance",
            "realistic complexion and features",
            "authentic natural appearance",
            "genuine skin tones and texture",
        ],
        "hair": [
            "with hair and facial hair as in reference",
            "hair cut and beard style matching reference",
            "original styling with scenario-appropriate grooming",
            "natural hair preserving length and facial hair",
        ],
        "expression": [
            "with confident natural expression",
            "showing authentic composed demeanor",
            "genuine engaging expression",
            "natural confident presence",
        ],
        "clothing": [
            "wearing scenario-appropriate attire reflecting the setting",
            "dressed authentically for the transformation context",
            "in styled clothing suited to the scenario",
            "with wardrobe choices matching the scene",
        ],
        "pose": [
            "positioned naturally in the scene",
            "positioned with confident presence",
            "naturally engaged with the setting",
            "comfortably positioned in the scenario",
        ],
        "environment": [
            "in a compelling transformation scenario",
            "within the scenic environment",
            "in the atmospheric setting",
            "situated in the scenario backdrop",
        ],
        "lighting": [
            "with strong natural lighting",
            "with dramatic cinematic lighting",
            "with professional atmospheric lighting",
            "with cinematic light quality",
        ],
        "mood": [
            "capturing authentic moment and presence",
            "conveying genuine narrative mood",
            "reflecting the scenario atmosphere",
            "showing powerful emotional resonance",
        ],
        "camera_style": [
            "professional portrait composition, 85mm focal length feel",
            "cinematic framing with depth",
            "professional photography aesthetic",
            "editorial quality composition",
        ],
        "color_palette": [
            "with sophisticated color grading and natural tones",
            "with cinematic color palette",
            "with professional color treatment",
            "with authentic scenario color tone",
        ],
        "quality_keywords": [
            "high definition, sharp detail, authentic photography",
            "masterpiece photography, award-winning quality",
            "professional portrait quality",
            "cinematic photography excellence",
        ]
    },
    
    # -----------------------------------------------------------------------
    # COUPLES TRANSFORMATION CATEGORY (couples_transform)
    # -----------------------------------------------------------------------
    "couples_transform": {
        "subject": [
            "Using reference images, transform the couple into a romantic intimate moment",
            "Using reference images, transform the couple into an adventure together",
            "Using reference images, capture the couple having joyful fun together",
            "Using reference images, transform the couple into a tender connection moment",
            "Based on reference images, reimagine the couple in a passionate scenario",
            "Based on reference images, reimagine the couple sharing a quiet intimate moment",
            "Reference images as base, transform the couple into a romantic setting",
            "Using both people from reference images in a beautiful couple scenario",
        ],
        "relationship_context": [
            "newlyweds celebrating their wedding",
            "long-time partners in committed romance",
            "childhood sweethearts reconnecting",
            "adventure partners exploring together",
            "parents capturing intimate family moment",
            "friends discovering secret connection",
            "professional partners with hidden chemistry",
            "distant lovers reunited by chance",
        ],
        "face_details": [
            "both with natural skin texture and appearance",
            "with realistic complexion and features for both",
            "both showing authentic natural appearance",
            "genuine natural appearance for both individuals",
        ],
        "hair": [
            "with hair matching reference appearance and length for both",
            "hair color and style as in reference images for both",
            "original hair preserving length and cut for both",
            "natural hair texture with scenario styling for both",
        ],
        "expression": [
            "with natural genuine expressions showing connection",
            "showing authentic affection and chemistry",
            "genuine relaxed expressions between them",
            "natural warm interaction between both",
        ],
        "clothing": [
            "wearing scenario-appropriate outfits for the couple",
            "dressed for the new scenario with coordinated styling",
            "styled appropriately for the couple setting",
            "in contextual costumes matching the scenario",
        ],
        "pose": [
            "positioned naturally showing couple connection",
            "positioned together in the scene authentically",
            "naturally engaged with each other and setting",
            "comfortably positioned showing relationship",
        ],
        "environment": [
            "in a beautiful couple transformation scenario",
            "within the scenic romantic environment",
            "in the atmospheric couple setting",
            "situated in the scenario backdrop together",
        ],
        "lighting": [
            "with warm romantic lighting flattering both",
            "with cinematic atmospheric lighting for couple",
            "with professional lighting enhancing connection",
            "with golden intimate lighting quality",
        ],
        "mood": [
            "capturing authentic couple moment and connection",
            "conveying genuine relationship and emotion",
            "reflecting the scenario with couple chemistry",
            "showing genuine emotional resonance between them",
        ],
        "camera_style": [
            "professional couple portrait composition, 85mm focal length feel",
            "cinematic framing showing connection and depth",
            "professional couple photography aesthetic",
            "editorial quality couple composition",
        ],
        "color_palette": [
            "with warm intimate color grading and natural tones",
            "with cinematic romantic color palette",
            "with professional balanced color treatment",
            "with authentic scenario color harmony",
        ],
        "quality_keywords": [
            "high definition, sharp detail, authentic couple photography",
            "masterpiece couple photography, award-winning quality",
            "professional couple portrait quality",
            "cinematic couple photography excellence",
        ]
    }
}


# ============================================================================
# COMPONENT SELECTOR & BUILDER FUNCTIONS
# ============================================================================

def get_component_template(category: str, component: str, subcategory: Optional[str] = None) -> List[str] or str:
    """
    Retrieve template options for a specific component in a category.
    
    Args:
        category: e.g., 'portrait_transformation', 'design_gifts', 'design_posters'
        component: e.g., 'subject', 'face_details', 'mood', 'lighting'
        subcategory: Optional subcategory for more specific options
        
    Returns:
        List of template strings or single string
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


def select_component(options: List[str] or str, preference: Optional[int] = None) -> str:
    """
    Select a single component from available options.
    
    Args:
        options: List of component options or single string
        preference: Optional index to select specific option (0-based)
        
    Returns:
        Selected component string
    """
    if isinstance(options, str):
        return options
    
    if isinstance(options, list):
        if preference is not None and 0 <= preference < len(options):
            return options[preference]
        # Default to first option if no preference
        return options[0]
    
    return str(options)


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
    
    # Component order for assembly
    component_order = [
        'subject', 'face_details', 'hair', 'expression', 'clothing',
        'pose', 'environment', 'lighting', 'mood', 'camera_style',
        'color_palette', 'quality_keywords'
    ]
    
    prompt_parts = []
    
    for component in component_order:
        if component == 'quality_keywords' and not include_quality:
            continue
        
        # Skip N/A components (not applicable for this category)
        templates = get_component_template(category, component)
        if templates == "N/A - skip for product designs unless featuring people" or \
           templates == "N/A - interface focus" or \
           templates == "N/A - design focus" or \
           templates == "N/A - product focus" or \
           templates == "N/A unless featuring portrait elements":
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
                    selected = selected[min(idx, len(selected) - 1)]
        else:
            idx = components.get(selection_key, 0)
            selected = select_component(templates, idx)
        
        if selected and selected != "N/A":
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
    component_order = [
        'subject', 'face_details', 'hair', 'expression', 'clothing',
        'pose', 'environment', 'lighting', 'mood', 'camera_style',
        'color_palette', 'quality_keywords'
    ]
    
    for component in component_order:
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
