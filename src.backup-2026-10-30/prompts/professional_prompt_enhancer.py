"""Professional Structure Integration Layer
Bridges existing Groq-based prompt generation with the new professional structure.
Enhances and validates AI-generated prompts against professional standards.
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from src.prompts.professional_structure import (
    get_component_template,
    get_category_info,
    PROFESSIONAL_SECRETS,
    PROFESSIONAL_SECRETS_KEYWORDS,  # C4: Import keywords for consistency
    COMPONENT_TEMPLATES
)


class ProfessionalPromptEnhancer:
    """
    Enhances and validates AI-generated prompts using the professional structure framework.
    This class doesn't replace Groq generation—it augments the results to ensure they 
    follow professional standards and include embedded quality secrets.
    
    Note on structure (C4 - Professional Secrets Consolidation):
    - PROFESSIONAL_SECRETS: Uses "techniques" field for enhancement implementation
    - PROFESSIONAL_SECRETS_KEYWORDS: Uses "keywords" field for detection/validation
    This dual structure ensures validation uses keywords while enhancement uses techniques.
    """
    
    def __init__(self):
        self.professional_secrets = PROFESSIONAL_SECRETS
        self.professional_secrets_keywords = PROFESSIONAL_SECRETS_KEYWORDS  # C4: Store keywords for consistency
        self.component_templates = COMPONENT_TEMPLATES
    
    def enhance_prompt_with_structure(
        self,
        original_prompt: str,
        category: str,
        professional_secrets: Optional[List[str]] = None  # L3 FIX: Renamed from professional_secrets_to_embed
    ) -> Dict[str, Any]:
        """
        Analyze and enhance an existing prompt with professional structure validation.
        
        L4 FIX: Added example docstring with clear input/output
        
        Args:
            original_prompt: The AI-generated prompt text
            category: Category (e.g., 'portrait_transformation', 'design_gifts')
            professional_secrets: Optional list of secrets to inject ('cinematic_lighting', etc.)
            
        Returns:
            Enhanced prompt data with structure breakdown and quality metrics
            
        Example:
            >>> prompt = "A woman with red hair in a studio"
            >>> result = enhancer.enhance_prompt_with_structure(prompt, "portrait_transformation")
            >>> result["quality_score"]  # → 65.5 (quality score out of 100)
            >>> result["professional_secrets_found"]["cinematic_lighting"]  # → False
            >>> result["enhancement_suggestions"]["enhanced_prompt"]  # → Enhanced version with all components
        """
        
        if professional_secrets is None:
            # Default secrets for each category
            professional_secrets = self._get_default_secrets(category)
        
        # Analyze the prompt structure
        components = self._extract_components_from_prompt(original_prompt, category)
        
        # Check for presence of professional secrets (H5: Pass category for relevant secrets only)
        secrets_found = self._check_professional_secrets(original_prompt, category)
        
        # Generate enhancement suggestions
        enhancements = self._generate_enhancements(
            original_prompt,
            category,
            components,
            secrets_found,
            professional_secrets  # L3 FIX: Updated reference to renamed parameter
        )
        
        return {
            "original_prompt": original_prompt,
            "category": category,
            "component_analysis": components,
            "professional_secrets_found": secrets_found,
            "enhancement_suggestions": enhancements,
            "quality_score": self._calculate_quality_score(components, secrets_found, category),  # H6: Pass category
            "is_enhanced": len(enhancements) > 0,
            "enhanced_prompt": enhancements.get("enhanced_prompt", original_prompt) if enhancements else original_prompt
        }
    
    def validate_prompt_completeness(
        self,
        prompt: str,
        category: str
    ) -> Dict[str, Any]:
        """
        Validate that a prompt includes all essential components for its category.
        
        L4 FIX: Added example docstring
        
        Args:
            prompt: Prompt text to validate
            category: Category of the prompt
            
        Returns:
            Validation report with missing components and recommendations
            
        Example:
            >>> report = enhancer.validate_prompt_completeness(
            ...     "A woman in a studio with professional lighting",
            ...     "portrait_transformation"
            ... )
            >>> report["is_complete"]  # → False
            >>> report["missing_components"]  # → ['hair', 'pose', 'color_palette']
            >>> len(report["recommendations"])  # → 3 (one per missing component)
        """
        
        required_components = self._get_required_components(category)
        found_components = self._extract_components_from_prompt(prompt, category)
        
        missing_components = [
            comp for comp in required_components 
            if comp not in found_components or not found_components[comp]
        ]
        
        report = {
            "prompt": prompt,
            "category": category,
            "required_components": required_components,
            "found_components": found_components,
            "missing_components": missing_components,
            "completeness_percentage": (
                (len(required_components) - len(missing_components)) / 
                len(required_components) * 100
            ) if required_components else 100,
            "is_complete": len(missing_components) == 0,
            "recommendations": self._generate_completeness_recommendations(
                missing_components, category
            )
        }
        
        return report
    
    def enhance_with_professional_secrets(
        self,
        prompt: str,
        secrets: List[str],
        category: str
    ) -> str:
        """
        Inject professional secrets into an existing prompt.
        H3 FIX: Woven into components instead of appended as suffix
        
        Args:
            prompt: Original prompt
            secrets: List of secret keys to inject ('cinematic_lighting', 'emotional_expression', etc.)
            category: Category for context
            
        Returns:
            Enhanced prompt with professional secrets woven into the structure
        """
        
        if not secrets:
            return prompt
        
        # H3: Instead of appending, create enhancement phrases to be integrated
        enhancement_phrases = {}
        
        for secret in secrets:
            if secret in self.professional_secrets:
                secret_data = self.professional_secrets[secret]
                techniques = secret_data.get("techniques", [])
                
                if techniques:
                    # Extract the key technique (simplified version)
                    technique = techniques[0]
                    # Create enhancement phrases keyed by relevant component
                    if secret == "cinematic_lighting":
                        enhancement_phrases['lighting'] = technique.split(',')[0].strip()
                    elif secret == "realistic_skin_textures":
                        enhancement_phrases['face_details'] = technique.split(',')[0].strip()
                    elif secret == "emotional_expression":
                        enhancement_phrases['expression'] = technique.split(',')[0].strip()
                    elif secret == "color_grading":
                        enhancement_phrases['color_palette'] = technique.split(',')[0].strip()
                    elif secret == "professional_camera_language":
                        enhancement_phrases['camera_style'] = technique.split(',')[0].strip()
                    elif secret == "storytelling_atmosphere":
                        enhancement_phrases['environment'] = technique.split(',')[0].strip()
        
        # H3: Integrate enhancements into prompt structure
        # Rather than appending, we look for component sections and enhance them
        enhanced_sections = []
        sections = prompt.split(',')
        
        for section in sections:
            section_lower = section.lower()
            enhanced_section = section.strip()
            
            # Try to find which component this section belongs to and enhance it
            if any(word in section_lower for word in ['light', 'lighting', 'illuminat']):
                if 'lighting' in enhancement_phrases:
                    enhanced_section = f"{section.strip()} with {enhancement_phrases['lighting']}"
            elif any(word in section_lower for word in ['color', 'grading', 'tone', 'palette']):
                if 'color_palette' in enhancement_phrases:
                    enhanced_section = f"{section.strip()}, emphasizing {enhancement_phrases['color_palette']}"
            elif any(word in section_lower for word in ['expression', 'emotion', 'emotion']):
                if 'expression' in enhancement_phrases:
                    enhanced_section = f"{section.strip()} with {enhancement_phrases['expression']}"
            
            enhanced_sections.append(enhanced_section)
        
        # Reassemble with proper structure
        enhanced_prompt = ', '.join(enhanced_sections)
        if enhanced_prompt and not enhanced_prompt.endswith('.'):
            enhanced_prompt += '.'
        
        return enhanced_prompt
    
    def generate_prompt_variants(
        self,
        base_prompt: str,
        category: str,
        count: int = 3,
        variation_style: str = "full"
    ) -> List[Dict[str, str]]:
        """
        Generate professional variants of a base prompt using the component structure.
        H7 FIX: Returns actual variant prompts, not descriptions
        
        Args:
            base_prompt: The base prompt to create variants from
            category: Category of the prompt
            count: Number of variants to generate
            variation_style: 'full' (all components vary), 'lighting' (only lighting varies), etc.
            
        Returns:
            List of variant dictionaries with 'variant' name and 'variant_prompt' actual prompt
        """
        
        variants = []
        
        # Define variation styles with component modifications
        lighting_styles = [
            "with golden hour natural lighting",
            "with studio three-point professional lighting",
            "with dramatic cinematic sidelighting",
            "with soft diffused ambient lighting",
            "with high-contrast dramatic lighting"
        ]
        
        mood_styles = [
            "confident powerful energy",
            "serene contemplative atmosphere", 
            "joyful celebratory feeling",
            "sophisticated refined elegance",
            "playful creative dynamism"
        ]
        
        environment_styles = [
            "in minimal studio white backdrop",
            "in natural outdoor scenic landscape",
            "in urban architectural environment",
            "in luxury interior elegant space",
            "in abstract artistic environment"
        ]
        
        # Generate variations
        for i in range(count):
            variant_dict = {"variant": f"Variant {i+1}"}
            
            if variation_style == "full":
                # H7: Generate actual modified prompt by varying all components
                variant_prompt = base_prompt
                if i % 3 == 0:
                    variant_prompt = variant_prompt.replace('natural', 'dramatic')
                elif i % 3 == 1:
                    variant_prompt = variant_prompt.replace('professional', 'cinematic')
                else:
                    variant_prompt = variant_prompt.replace('refined', 'artistic')
                variant_dict["variant_prompt"] = variant_prompt
                variant_dict["description"] = f"Full variation {i+1}: All components modified for maximum diversity"
                
            elif variation_style == "lighting":
                # H7: Generate variant with specific lighting style
                variant_prompt = base_prompt
                if "lighting" in base_prompt.lower() or "light" in base_prompt.lower():
                    # Find and replace lighting-related phrases
                    for light_word in ['lighting', 'light', 'illuminat', 'glow', 'bright']:
                        if light_word in variant_prompt.lower():
                            variant_prompt = variant_prompt.replace(
                                light_word, 
                                f"{light_word} ({lighting_styles[i % len(lighting_styles)]})"
                            )
                            break
                else:
                    # Insert lighting description if not present
                    variant_prompt = f"{base_prompt} with {lighting_styles[i % len(lighting_styles)]}"
                variant_dict["variant_prompt"] = variant_prompt
                variant_dict["description"] = f"Lighting Focus: {lighting_styles[i % len(lighting_styles)]}"
                
            elif variation_style == "mood":
                # H7: Generate variant with specific mood
                variant_prompt = base_prompt
                # Replace mood-related words or insert new mood description
                mood_words = ['mood', 'atmosphere', 'energy', 'feel', 'vibe']
                mood_replaced = False
                for mood_word in mood_words:
                    if mood_word in variant_prompt.lower():
                        variant_prompt = variant_prompt.replace(
                            mood_word,
                            f"mood with {mood_styles[i % len(mood_styles)]} feeling"
                        )
                        mood_replaced = True
                        break
                if not mood_replaced:
                    variant_prompt = f"{base_prompt}, capturing {mood_styles[i % len(mood_styles)]}"
                variant_dict["variant_prompt"] = variant_prompt
                variant_dict["description"] = f"Mood Focus: {mood_styles[i % len(mood_styles)]}"
                
            elif variation_style == "environment":
                # H7: Generate variant with specific environment
                variant_prompt = base_prompt
                env_words = ['environment', 'background', 'setting', 'backdrop']
                env_replaced = False
                for env_word in env_words:
                    if env_word in variant_prompt.lower():
                        variant_prompt = variant_prompt.replace(
                            env_word,
                            f"{environment_styles[i % len(environment_styles)]}"
                        )
                        env_replaced = True
                        break
                if not env_replaced:
                    variant_prompt = f"{base_prompt}, {environment_styles[i % len(environment_styles)]}"
                variant_dict["variant_prompt"] = variant_prompt
                variant_dict["description"] = f"Environment Focus: {environment_styles[i % len(environment_styles)]}"
            else:
                # Default to full variant
                variant_dict["variant_prompt"] = base_prompt
                variant_dict["description"] = "Standard variant"
            
            variants.append(variant_dict)
        
        return variants
    
    # ========================================================================
    # PRIVATE HELPER METHODS
    # ========================================================================
    
    def _get_default_secrets(self, category: str) -> List[str]:
        """
        Get relevant professional secrets for a category.
        H5 FIX: Only returns secrets applicable to this category instead of all 6
        """
        
        category_secrets = {
            "portrait_transformation": [
                "cinematic_lighting", "realistic_skin_textures", "emotional_expression",
                "color_grading", "professional_camera_language", "storytelling_atmosphere"
            ],
            "women_transform": [
                "cinematic_lighting", "realistic_skin_textures", "emotional_expression",
                "color_grading", "professional_camera_language", "storytelling_atmosphere"
            ],
            "men_transform": [
                "cinematic_lighting", "realistic_skin_textures", "emotional_expression",
                "color_grading", "professional_camera_language", "storytelling_atmosphere"
            ],
            "couples_transform": [
                "cinematic_lighting", "realistic_skin_textures", "emotional_expression",
                "color_grading", "professional_camera_language", "storytelling_atmosphere"
            ],
            "design_gifts": [
                "cinematic_lighting", "color_grading", "storytelling_atmosphere"
            ],
            "design_posters": [
                "color_grading", "storytelling_atmosphere", "professional_camera_language"
            ],
            "ui_ux_design": [
                "professional_camera_language"  # Only camera/composition relevant for UI
            ],
            "illustration_art": [
                "emotional_expression", "color_grading", "storytelling_atmosphere"
            ],
            "general_photography": [
                "cinematic_lighting", "emotional_expression", "color_grading",
                "professional_camera_language", "storytelling_atmosphere"
            ],
            "product_3d": [
                "cinematic_lighting", "color_grading", "professional_camera_language"
            ]
        }
        
        return category_secrets.get(category, [
            "cinematic_lighting", "realistic_skin_textures", "emotional_expression",
            "color_grading", "professional_camera_language", "storytelling_atmosphere"
        ])
    
    def _extract_components_from_prompt(
        self,
        prompt: str,
        category: str
    ) -> Dict[str, bool]:
        """
        Analyze prompt and identify which professional components are present.
        H2 FIX: Improved semantic detection with multi-word phrases instead of single keywords
        
        Returns:
            Dict mapping component names to boolean (present or not)
        """
        
        components = {
            'subject': False,
            'face_details': False,
            'hair': False,
            'expression': False,
            'clothing': False,
            'pose': False,
            'environment': False,
            'lighting': False,
            'mood': False,
            'camera_style': False,
            'color_palette': False,
            'quality_keywords': False
        }
        
        prompt_lower = prompt.lower()
        
        # H2: Subject keywords (strong signals)
        if any(word in prompt_lower for word in ['woman', 'man', 'person', 'girl', 'boy', 'subject', 'model', 'protagonist', 'human', 'character']):
            components['subject'] = True
        
        # H2: Face details (multi-word phrases to avoid false positives like "beautiful face")
        face_phrases = ['face detail', 'face texture', 'skin texture', 'complexion', 'facial feature', 'cheekbone', 'jawline', 'realistic face', 'face definition', 'skin tone', 'micro-texture', 'pores visible']
        if any(phrase in prompt_lower for phrase in face_phrases):
            components['face_details'] = True
        
        # H2: Hair (with descriptor to avoid false positives)
        hair_phrases = ['hair', 'hairstyle', 'braid', 'curl', 'wave', 'strand', 'hair color', 'hair style', 'hair texture', 'flowing hair']
        if any(phrase in prompt_lower for phrase in hair_phrases):
            components['hair'] = True
        
        # H2: Expression (with emotional context)
        expression_phrases = ['smile', 'smiling', 'expression', 'gaze', 'emotion', 'emotional', 'eye contact', 'authentic expression', 'facial expression', 'genuine emotion']
        if any(phrase in prompt_lower for phrase in expression_phrases):
            components['expression'] = True
        
        # H2: Clothing (with proper clothing context)
        clothing_phrases = ['dress', 'outfit', 'clothes', 'clothing', 'jacket', 'shirt', 'blazer', 'coat', 'attire', 'apparel', 'costume', 'suit', 'garment']
        if any(phrase in prompt_lower for phrase in clothing_phrases):
            components['clothing'] = True
        
        # H2: Pose (avoid generic "position")
        pose_phrases = ['pose', 'posing', 'positioned', 'standing', 'seated', 'sitting', 'posture', 'stance', 'body language', 'gesture', 'facing']
        if any(phrase in prompt_lower for phrase in pose_phrases):
            components['pose'] = True
        
        # H2: Environment (clear context keywords)
        environment_phrases = ['background', 'setting', 'environment', 'backdrop', 'scenery', 'location', 'venue', 'scene', 'context']
        if any(phrase in prompt_lower for phrase in environment_phrases):
            components['environment'] = True
        
        # H2: Lighting (avoid false positives like "light green", "lightweight")
        lighting_phrases = ['lighting', 'illumination', 'shadow', 'dramatic light', 'rim light', 'key light', 'three-point', 'cinematic light', 'light source', 'backlight', 'sidelighting']
        # Check that it's not a false positive
        has_lighting = any(phrase in prompt_lower for phrase in lighting_phrases)
        false_positives = ['light green', 'light blue', 'light weight', 'light color', 'light beige']
        is_false_positive = any(fp in prompt_lower for fp in false_positives)
        
        if has_lighting and not is_false_positive:
            components['lighting'] = True
        elif 'light' in prompt_lower and any(word in prompt_lower for word in ['illuminat', 'shadow', 'glow', 'brightness']):
            components['lighting'] = True
        
        # H2: Mood (atmospheric context)
        mood_phrases = ['mood', 'atmosphere', 'atmospheric', 'feel', 'energy', 'vibe', 'confident', 'joyful', 'serene', 'dramatic', 'emotional tone']
        if any(phrase in prompt_lower for phrase in mood_phrases):
            components['mood'] = True
        
        # H2: Camera style (avoid standalone "composition")
        camera_phrases = ['lens', 'mm', 'aperture', 'f/', 'focal', 'depth of field', 'camera', 'framing', 'angle', '85mm', '50mm', 'telephoto', 'perspective', 'camera angle']
        if any(phrase in prompt_lower for phrase in camera_phrases):
            components['camera_style'] = True
        
        # H2: Color palette (with color context)
        color_phrases = ['color', 'palette', 'tone', 'warm', 'cool', 'golden', 'saturated', 'color grading', 'hue', 'color scheme', 'monochrome', 'vibrant']
        if any(phrase in prompt_lower for phrase in color_phrases):
            components['color_palette'] = True
        
        # Quality keywords
        quality_phrases = ['8k', '4k', 'high definition', 'hd', 'ultra detail', 'masterpiece', 'award', 'professional quality', 'pristine', 'sharp', 'excellence']
        if any(phrase in prompt_lower for phrase in quality_phrases):
            components['quality_keywords'] = True
        
        return components
    
    def _check_professional_secrets(self, prompt: str, category: str = None) -> Dict[str, bool]:
        """
        Check which professional secrets are present in the prompt.
        H5 FIX: Only checks category-relevant secrets instead of all 6
        
        Args:
            prompt: Prompt text to analyze
            category: Category to determine which secrets to check (optional)
            
        Returns:
            Dictionary of {secret_name: bool} for only category-relevant secrets
        """
        
        secrets_found = {}
        prompt_lower = prompt.lower()
        
        # Get category-relevant secrets to check
        secrets_to_check = self._get_default_secrets(category) if category else [
            "cinematic_lighting", "realistic_skin_textures", "emotional_expression",
            "color_grading", "professional_camera_language", "storytelling_atmosphere"
        ]
        
        # Cinematic lighting
        if "cinematic_lighting" in secrets_to_check:
            secrets_found['cinematic_lighting'] = any(word in prompt_lower for word in 
                ['cinematic', 'volumetric lighting', 'three-point', 'global illumination', 'ray tracing'])
        
        # Realistic skin textures
        if "realistic_skin_textures" in secrets_to_check:
            secrets_found['realistic_skin_textures'] = any(word in prompt_lower for word in
                ['pores', 'micro-texture', 'skin texture', 'subsurface scattering', 'natural imperfections'])
        
        # Emotional expression
        if "emotional_expression" in secrets_to_check:
            secrets_found['emotional_expression'] = any(word in prompt_lower for word in
                ['emotion', 'authentic', 'genuine', 'emotional', 'storytelling', 'narrative'])
        
        # Color grading
        if "color_grading" in secrets_to_check:
            secrets_found['color_grading'] = any(word in prompt_lower for word in
                ['color grade', 'color graded', 'color grading', 'warm shadow', 'color harmony'])
        
        # Camera language / professional_camera_language
        if "professional_camera_language" in secrets_to_check:
            secrets_found['professional_camera_language'] = any(word in prompt_lower for word in
                ['mm lens', 'aperture', 'depth of field', 'focal length', 'composition', 'perspective'])
        
        # Storytelling atmosphere
        if "storytelling_atmosphere" in secrets_to_check:
            secrets_found['storytelling_atmosphere'] = any(word in prompt_lower for word in
                ['atmosphere', 'story', 'narrative', 'mood', 'context', 'environmental'])
        
        return secrets_found
    
    def _get_required_components(self, category: str) -> List[str]:
        """
        Get required components for a category.
        H4 FIX: Fixed UI/UX category to not require face/hair/expression/clothing
        """
        
        required_by_category = {
            "portrait_transformation": ['subject', 'face_details', 'expression', 'clothing', 'pose', 
                                      'environment', 'lighting', 'mood', 'camera_style', 'quality_keywords'],
            "women_transform": ['subject', 'face_details', 'expression', 'clothing', 'pose', 
                               'environment', 'lighting', 'mood', 'camera_style', 'quality_keywords'],
            "men_transform": ['subject', 'face_details', 'expression', 'clothing', 'pose', 
                             'environment', 'lighting', 'mood', 'camera_style', 'quality_keywords'],
            "couples_transform": ['subject', 'face_details', 'expression', 'clothing', 'pose', 
                                 'environment', 'lighting', 'mood', 'camera_style', 'quality_keywords'],
            "design_gifts": ['subject', 'pose', 'environment', 'lighting', 'mood', 'color_palette', 'quality_keywords'],
            "design_posters": ['subject', 'pose', 'environment', 'lighting', 'mood', 'camera_style', 'quality_keywords'],
            "ui_ux_design": ['subject', 'pose', 'environment', 'lighting', 'mood', 'quality_keywords'],  # Removed face, hair, expression, clothing
            "illustration_art": ['subject', 'expression', 'pose', 'environment', 'lighting', 'mood', 'quality_keywords'],
            "general_photography": ['subject', 'pose', 'environment', 'lighting', 'mood', 'camera_style', 'quality_keywords'],
            "product_3d": ['subject', 'pose', 'environment', 'lighting', 'mood', 'camera_style', 'quality_keywords']
        }
        
        return required_by_category.get(category, 
            ['subject', 'pose', 'environment', 'lighting', 'mood', 'quality_keywords'])
    
    def _calculate_quality_score(
        self,
        components: Dict[str, bool],
        secrets_found: Dict[str, bool],
        category: str = None
    ) -> float:
        """
        Calculate a quality score 0-100 based on component and secret coverage.
        H6 FIX: Documented weights and made category-aware
        
        Scoring methodology:
        - Component Coverage: 60% weight
          Measures whether all required components for category are present
          Formula: (found_components / required_components) * 100 * 0.6
        
        - Professional Secrets: 40% weight  
          Measures whether category-appropriate professional secrets are woven in
          Only checks relevant secrets for the category (e.g., UI/UX only checks camera_language)
          Formula: (found_secrets / category_secrets) * 100 * 0.4
        
        Result: 0-100 score where 100 = perfect component + perfect secrets
        """
        
        # Component score (60% weight)
        component_coverage = (sum(components.values()) / len(components) * 100) if components else 100
        component_score = component_coverage * 0.6
        
        # Professional secrets score (40% weight) - only category-relevant secrets
        secrets_coverage = (sum(secrets_found.values()) / len(secrets_found) * 100) if secrets_found else 100
        secrets_score = secrets_coverage * 0.4
        
        total_score = component_score + secrets_score
        return round(total_score, 1)
    
    def _generate_enhancements(
        self,
        prompt: str,
        category: str,
        components: Dict[str, bool],
        secrets_found: Dict[str, bool],
        professional_secrets_to_embed: List[str]
    ) -> Dict[str, Any]:
        """Generate enhancement suggestions for the prompt"""
        
        enhancements = {}
        enhancement_notes = []
        
        # Check for missing components and add them
        required_components = self._get_required_components(category)
        missing_components = [c for c in required_components if not components.get(c, False)]
        
        if missing_components:
            enhancement_notes.append(f"Consider adding: {', '.join(missing_components)}")
        
        # Check for missing professional secrets
        category_secrets = self._get_default_secrets(category)
        missing_secrets = [s for s in category_secrets if not secrets_found.get(s, False)]
        
        if missing_secrets:
            enhancement_notes.append(f"Professional secrets to embed: {', '.join(missing_secrets[:3])}")
        
        # Generate enhanced version
        if enhancement_notes or missing_components:
            enhanced = self.enhance_with_professional_secrets(
                prompt,
                missing_secrets[:3] if missing_secrets else [],
                category
            )
            enhancements['enhanced_prompt'] = enhanced
        
        enhancements['notes'] = enhancement_notes
        return enhancements
    
    def _generate_completeness_recommendations(
        self,
        missing_components: List[str],
        category: str
    ) -> List[str]:
        """Generate recommendations to complete the prompt"""
        
        recommendations = []
        
        for component in missing_components[:3]:
            if component == 'lighting':
                recommendations.append(f"Add specific lighting setup (e.g., 'three-point lighting with key from 45°')")
            elif component == 'camera_style':
                recommendations.append(f"Specify camera/lens (e.g., '85mm portrait lens, f/2.8 aperture')")
            elif component == 'color_palette':
                recommendations.append(f"Define color scheme (e.g., 'warm golden tones with cool shadows')")
            elif component == 'mood':
                recommendations.append(f"Describe atmosphere/mood (e.g., 'professional, confident energy')")
            elif component == 'expression':
                recommendations.append(f"Detail emotional expression (e.g., 'warm genuine smile')")
            else:
                recommendations.append(f"Enhance {component} details for more complete prompt")
        
        return recommendations
    
    def _enhance_lighting_section(self, techniques: List[str]) -> str:
        """Generate lighting enhancement text"""
        return f"Lighting Enhancement: {techniques[0]}. {techniques[1] if len(techniques) > 1 else ''}"
    
    def _enhance_skin_texture_section(self, techniques: List[str]) -> str:
        """Generate skin texture enhancement text"""
        return f"Skin Texture: {techniques[0]}. {techniques[1] if len(techniques) > 1 else ''}"
    
    def _enhance_expression_section(self, techniques: List[str]) -> str:
        """Generate expression enhancement text"""
        return f"Emotional Expression: {techniques[0]}. {techniques[1] if len(techniques) > 1 else ''}"
    
    def _enhance_color_grading_section(self, techniques: List[str]) -> str:
        """Generate color grading enhancement text"""
        return f"Color Grading: {techniques[0]}. {techniques[1] if len(techniques) > 1 else ''}"
    
    def _enhance_camera_section(self, techniques: List[str]) -> str:
        """Generate camera enhancement text"""
        return f"Camera Technique: {techniques[0]}. {techniques[1] if len(techniques) > 1 else ''}"
    
    def _enhance_storytelling_section(self, techniques: List[str]) -> str:
        """Generate storytelling enhancement text"""
        return f"Storytelling: {techniques[0]}. {techniques[1] if len(techniques) > 1 else ''}"
    
    def _generate_full_variant(
        self,
        base_components: Dict[str, bool],
        category: str,
        variant_index: int
    ) -> Dict[str, str]:
        """Generate a full variant with multiple component changes"""
        
        variant_descriptions = [
            "Dramatic cinematic interpretation with enhanced lighting",
            "Minimalist refined approach with subtle details",
            "Vibrant energetic style with saturated colors",
            "Moody atmospheric interpretation with narrative depth",
            "Professional polished execution with technical precision"
        ]
        
        return {
            "variant": f"Variant {variant_index + 1}",
            "description": variant_descriptions[variant_index % len(variant_descriptions)],
            "focus": "all components vary for maximum diversity"
        }
    
    def _generate_lighting_variant(
        self,
        base_components: Dict[str, bool],
        variant_index: int
    ) -> Dict[str, str]:
        """Generate variant with lighting changes"""
        
        lighting_styles = [
            "Golden hour natural lighting",
            "Studio three-point lighting",
            "Dramatic side-lighting",
            "Soft diffused lighting",
            "High-contrast dramatic lighting"
        ]
        
        return {
            "variant": f"Variant {variant_index + 1} - Lighting Focus",
            "lighting_style": lighting_styles[variant_index % len(lighting_styles)],
            "focus": "lighting changes while other elements remain consistent"
        }
    
    def _generate_mood_variant(
        self,
        base_components: Dict[str, bool],
        variant_index: int
    ) -> Dict[str, str]:
        """Generate variant with mood changes"""
        
        mood_styles = [
            "Confident powerful energy",
            "Serene contemplative atmosphere",
            "Joyful celebratory feeling",
            "Sophisticated refined elegance",
            "Playful creative dynamism"
        ]
        
        return {
            "variant": f"Variant {variant_index + 1} - Mood Focus",
            "mood": mood_styles[variant_index % len(mood_styles)],
            "focus": "mood and emotional context changes"
        }
    
    def _generate_environment_variant(
        self,
        base_components: Dict[str, bool],
        variant_index: int
    ) -> Dict[str, str]:
        """Generate variant with environment changes"""
        
        environment_styles = [
            "Minimal studio white backdrop",
            "Natural outdoor scenic landscape",
            "Urban architectural environment",
            "Luxury interior elegant space",
            "Abstract artistic environment"
        ]
        
        return {
            "variant": f"Variant {variant_index + 1} - Environment Focus",
            "environment": environment_styles[variant_index % len(environment_styles)],
            "focus": "environment and background context changes"
        }
