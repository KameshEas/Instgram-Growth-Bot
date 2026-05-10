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
    COMPONENT_TEMPLATES
)


class ProfessionalPromptEnhancer:
    """
    Enhances and validates AI-generated prompts using the professional structure framework.
    This class doesn't replace Groq generation—it augments the results to ensure they 
    follow professional standards and include embedded quality secrets.
    """
    
    def __init__(self):
        self.professional_secrets = PROFESSIONAL_SECRETS
        self.component_templates = COMPONENT_TEMPLATES
    
    def enhance_prompt_with_structure(
        self,
        original_prompt: str,
        category: str,
        professional_secrets_to_embed: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze and enhance an existing prompt with professional structure validation.
        
        Args:
            original_prompt: The AI-generated prompt text
            category: Category (e.g., 'portrait_transformation', 'design_gifts')
            professional_secrets_to_embed: Optional list of secrets to inject ('cinematic_lighting', etc.)
            
        Returns:
            Enhanced prompt data with structure breakdown and quality metrics
        """
        
        if professional_secrets_to_embed is None:
            # Default secrets for each category
            professional_secrets_to_embed = self._get_default_secrets(category)
        
        # Analyze the prompt structure
        components = self._extract_components_from_prompt(original_prompt, category)
        
        # Check for presence of professional secrets
        secrets_found = self._check_professional_secrets(original_prompt)
        
        # Generate enhancement suggestions
        enhancements = self._generate_enhancements(
            original_prompt,
            category,
            components,
            secrets_found,
            professional_secrets_to_embed
        )
        
        return {
            "original_prompt": original_prompt,
            "category": category,
            "component_analysis": components,
            "professional_secrets_found": secrets_found,
            "enhancement_suggestions": enhancements,
            "quality_score": self._calculate_quality_score(components, secrets_found),
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
        
        Args:
            prompt: Prompt text to validate
            category: Category of the prompt
            
        Returns:
            Validation report with missing components and recommendations
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
        
        Args:
            prompt: Original prompt
            secrets: List of secret keys to inject ('cinematic_lighting', 'emotional_expression', etc.)
            category: Category for context
            
        Returns:
            Enhanced prompt with professional secrets woven in
        """
        
        enhancement_injection = ""
        
        for secret in secrets:
            if secret in self.professional_secrets:
                secret_data = self.professional_secrets[secret]
                techniques = secret_data.get("techniques", [])
                
                # Select 1-2 most relevant techniques
                selected_techniques = techniques[:2]
                
                # Determine where to inject based on the secret
                if secret == "cinematic_lighting":
                    enhancement_injection += self._enhance_lighting_section(
                        selected_techniques
                    )
                elif secret == "realistic_skin_textures":
                    enhancement_injection += self._enhance_skin_texture_section(
                        selected_techniques
                    )
                elif secret == "emotional_expression":
                    enhancement_injection += self._enhance_expression_section(
                        selected_techniques
                    )
                elif secret == "color_grading":
                    enhancement_injection += self._enhance_color_grading_section(
                        selected_techniques
                    )
                elif secret == "camera_language":
                    enhancement_injection += self._enhance_camera_section(
                        selected_techniques
                    )
                elif secret == "storytelling_atmosphere":
                    enhancement_injection += self._enhance_storytelling_section(
                        selected_techniques
                    )
        
        # Combine with original prompt
        if enhancement_injection:
            enhanced = f"{prompt}\n\n[Professional Enhancement]: {enhancement_injection}"
            return enhanced
        
        return prompt
    
    def generate_prompt_variants(
        self,
        base_prompt: str,
        category: str,
        count: int = 3,
        variation_style: str = "full"
    ) -> List[Dict[str, str]]:
        """
        Generate professional variants of a base prompt using the component structure.
        
        Args:
            base_prompt: The base prompt to create variants from
            category: Category of the prompt
            count: Number of variants to generate
            variation_style: 'full' (all components vary), 'lighting' (only lighting varies), etc.
            
        Returns:
            List of variant prompts with descriptions
        """
        
        variants = []
        
        # Extract base components
        base_components = self._extract_components_from_prompt(base_prompt, category)
        
        # Generate variations
        for i in range(count):
            if variation_style == "full":
                variant = self._generate_full_variant(base_components, category, i)
            elif variation_style == "lighting":
                variant = self._generate_lighting_variant(base_components, i)
            elif variation_style == "mood":
                variant = self._generate_mood_variant(base_components, i)
            elif variation_style == "environment":
                variant = self._generate_environment_variant(base_components, i)
            else:
                variant = self._generate_full_variant(base_components, category, i)
            
            variants.append(variant)
        
        return variants
    
    # ========================================================================
    # PRIVATE HELPER METHODS
    # ========================================================================
    
    def _get_default_secrets(self, category: str) -> List[str]:
        """Get default professional secrets for a category"""
        
        default_secrets_by_category = {
            "portrait_transformation": [
                "cinematic_lighting",
                "realistic_skin_textures",
                "emotional_expression",
                "color_grading",
                "camera_language",
                "storytelling_atmosphere"
            ],
            "design_gifts": [
                "cinematic_lighting",
                "color_grading",
                "storytelling_atmosphere"
            ],
            "design_posters": [
                "color_grading",
                "storytelling_atmosphere",
                "camera_language"
            ],
            "ui_ux_design": [
                "camera_language"
            ],
            "illustration_art": [
                "emotional_expression",
                "color_grading",
                "storytelling_atmosphere"
            ],
            "general_photography": [
                "cinematic_lighting",
                "emotional_expression",
                "color_grading",
                "camera_language",
                "storytelling_atmosphere"
            ],
            "product_3d": [
                "cinematic_lighting",
                "color_grading",
                "camera_language"
            ]
        }
        
        return default_secrets_by_category.get(category, [])
    
    def _extract_components_from_prompt(
        self,
        prompt: str,
        category: str
    ) -> Dict[str, bool]:
        """
        Analyze prompt and identify which professional components are present.
        
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
        
        # Subject/person keywords
        if any(word in prompt_lower for word in ['woman', 'man', 'person', 'girl', 'boy', 'subject', 'model']):
            components['subject'] = True
        
        # Face/skin keywords
        if any(word in prompt_lower for word in ['face', 'skin', 'cheekbone', 'jawline', 'complexion', 'features']):
            components['face_details'] = True
        
        # Hair keywords
        if any(word in prompt_lower for word in ['hair', 'hairstyle', 'braid', 'curl', 'wave', 'strand']):
            components['hair'] = True
        
        # Expression keywords
        if any(word in prompt_lower for word in ['smile', 'expression', 'gaze', 'emotion', 'eye', 'look']):
            components['expression'] = True
        
        # Clothing keywords
        if any(word in prompt_lower for word in ['dress', 'outfit', 'clothes', 'jacket', 'shirt', 'blazer', 'coat', 'attire']):
            components['clothing'] = True
        
        # Pose keywords
        if any(word in prompt_lower for word in ['pose', 'standing', 'seated', 'posture', 'position', 'stance']):
            components['pose'] = True
        
        # Environment keywords
        if any(word in prompt_lower for word in ['background', 'setting', 'environment', 'space', 'venue', 'location']):
            components['environment'] = True
        
        # Lighting keywords
        if any(word in prompt_lower for word in ['light', 'lighting', 'shadow', 'illumination', 'glow', 'bright']):
            components['lighting'] = True
        
        # Mood keywords
        if any(word in prompt_lower for word in ['mood', 'atmosphere', 'feel', 'energy', 'vibe', 'confident', 'radiant']):
            components['mood'] = True
        
        # Camera style keywords
        if any(word in prompt_lower for word in ['lens', 'mm', 'aperture', 'f/', 'depth', 'field', 'composition', 'angle']):
            components['camera_style'] = True
        
        # Color palette keywords
        if any(word in prompt_lower for word in ['color', 'palette', 'tone', 'warm', 'cool', 'golden', 'saturated']):
            components['color_palette'] = True
        
        # Quality keywords
        if any(word in prompt_lower for word in ['8k', '4k', 'high definition', 'hd', 'ultra detailed', 'masterpiece', 'award']):
            components['quality_keywords'] = True
        
        return components
    
    def _check_professional_secrets(self, prompt: str) -> Dict[str, bool]:
        """Check which professional secrets are present in the prompt"""
        
        secrets_found = {}
        prompt_lower = prompt.lower()
        
        # Cinematic lighting
        secrets_found['cinematic_lighting'] = any(word in prompt_lower for word in 
            ['cinematic', 'volumetric lighting', 'three-point', 'global illumination', 'ray tracing'])
        
        # Realistic skin textures
        secrets_found['realistic_skin_textures'] = any(word in prompt_lower for word in
            ['pores', 'micro-texture', 'skin texture', 'subsurface scattering', 'natural imperfections'])
        
        # Emotional expression
        secrets_found['emotional_expression'] = any(word in prompt_lower for word in
            ['emotion', 'authentic', 'genuine', 'emotional', 'storytelling', 'narrative'])
        
        # Color grading
        secrets_found['color_grading'] = any(word in prompt_lower for word in
            ['color grade', 'color graded', 'color grading', 'warm shadow', 'color harmony'])
        
        # Camera language
        secrets_found['camera_language'] = any(word in prompt_lower for word in
            ['mm lens', 'aperture', 'depth of field', 'focal length', 'composition', 'perspective'])
        
        # Storytelling atmosphere
        secrets_found['storytelling_atmosphere'] = any(word in prompt_lower for word in
            ['atmosphere', 'story', 'narrative', 'mood', 'context', 'environmental'])
        
        return secrets_found
    
    def _get_required_components(self, category: str) -> List[str]:
        """Get required components for a category"""
        
        required_by_category = {
            "portrait_transformation": ['subject', 'face_details', 'expression', 'clothing', 'pose', 
                                      'environment', 'lighting', 'mood', 'camera_style', 'quality_keywords'],
            "design_gifts": ['subject', 'pose', 'environment', 'lighting', 'mood', 'color_palette', 'quality_keywords'],
            "design_posters": ['subject', 'pose', 'environment', 'lighting', 'mood', 'camera_style', 'quality_keywords'],
            "ui_ux_design": ['subject', 'pose', 'environment', 'lighting', 'mood', 'quality_keywords'],
            "illustration_art": ['subject', 'expression', 'pose', 'environment', 'lighting', 'mood', 'quality_keywords'],
            "general_photography": ['subject', 'pose', 'environment', 'lighting', 'mood', 'camera_style', 'quality_keywords'],
            "product_3d": ['subject', 'pose', 'environment', 'lighting', 'mood', 'camera_style', 'quality_keywords']
        }
        
        return required_by_category.get(category, 
            ['subject', 'pose', 'environment', 'lighting', 'mood', 'quality_keywords'])
    
    def _calculate_quality_score(
        self,
        components: Dict[str, bool],
        secrets_found: Dict[str, bool]
    ) -> float:
        """
        Calculate a quality score 0-100 based on component and secret coverage.
        """
        
        # Weight: 60% components, 40% professional secrets
        component_score = (sum(components.values()) / len(components) * 100) * 0.6
        secrets_score = (sum(secrets_found.values()) / len(secrets_found) * 100) * 0.4
        
        return round(component_score + secrets_score, 1)
    
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
