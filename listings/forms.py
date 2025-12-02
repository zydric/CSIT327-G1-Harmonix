from django import forms
from django.core.exceptions import ValidationError
from .models import Listing
from harmonix.constants import GENRE_CHOICES, INSTRUMENT_CHOICES


class CustomMultipleChoiceField(forms.MultipleChoiceField):
    """
    Custom MultipleChoiceField that allows values not in predefined choices
    """
    def validate(self, value):
        # Override to allow custom values
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')


class ListingForm(forms.ModelForm):
    """
    Form for creating and editing band listings
    """
    # Override fields to use custom multi-select widgets that allow custom values
    instruments_needed = CustomMultipleChoiceField(
        choices=INSTRUMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'w-4 h-4 text-purple-600 bg-white border-gray-300 rounded focus:ring-purple-500 focus:ring-2'
        }),
        help_text="Select all instruments needed for this opportunity"
    )
    
    genres = CustomMultipleChoiceField(
        choices=GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'w-4 h-4 text-indigo-600 bg-white border-gray-300 rounded focus:ring-indigo-500 focus:ring-2'
        }),
        help_text="Select all genres that describe your band's style"
    )

    class Meta:
        model = Listing
        fields = ['title', 'band_name', 'description', 'location', 'instruments_needed', 'genres', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-gray-900 font-medium transition-colors',
                'placeholder': 'e.g., "Lead Guitarist Needed for Rock Band"'
            }),
            'band_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-gray-900 font-medium transition-colors',
                'placeholder': 'Your band name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-gray-900 leading-relaxed transition-colors',
                'rows': 6,
                'placeholder': 'Describe the opportunity, requirements, and what you\'re looking for in detail...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 text-gray-900 font-medium transition-colors',
                'placeholder': 'e.g., "Sugbo Mercado, Sea Grove, JPark Resort"'
            }),
        }
        # help_texts = {
        #     'title': 'Create an engaging title that clearly describes the opportunity',
        #     'band_name': 'The name of your band or musical project',
        #     'description': 'Provide detailed information about the opportunity, requirements, and expectations',
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial values for multi-select fields if editing
        if self.instance and self.instance.pk:
            # Convert comma-separated strings back to lists for editing
            if self.instance.instruments_needed:
                self.fields['instruments_needed'].initial = [
                    instrument.strip().lower() 
                    for instrument in self.instance.instruments_needed.split(',')
                    if instrument.strip()
                ]
            
            if self.instance.genres:
                self.fields['genres'].initial = [
                    genre.strip().lower()
                    for genre in self.instance.genres.split(',')
                    if genre.strip()
                ]
        else:
            # For new listings, remove is_active field (will default to True in model)
            self.fields.pop('is_active', None)

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError("Title is required.")
        
        if len(title.strip()) < 10:
            raise ValidationError("Title must be at least 10 characters long.")
        
        if len(title.strip()) > 80:
            raise ValidationError("Title cannot exceed 80 characters.")
        
        return title.strip()

    def clean_band_name(self):
        band_name = self.cleaned_data.get('band_name')
        if not band_name:
            raise ValidationError("Band name is required.")
        
        if len(band_name.strip()) < 2:
            raise ValidationError("Band name must be at least 2 characters long.")
        
        if len(band_name.strip()) > 50:
            raise ValidationError("Band name cannot exceed 50 characters.")
        
        return band_name.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise ValidationError("Description is required.")
        
        if len(description.strip()) < 50:
            raise ValidationError("Description must be at least 50 characters long to provide enough detail.")
        
        if len(description.strip()) > 500:
            raise ValidationError("Description cannot exceed 500 characters.")
        
        return description.strip()

    def clean_instruments_needed(self):
        instruments = self.cleaned_data.get('instruments_needed')
        if not instruments:
            raise ValidationError("At least one instrument must be selected.")
        
        if len(instruments) > 3:
            raise ValidationError("Maximum 3 instruments can be selected. Choose your primary needs.")
        
        return instruments

    def clean_genres(self):
        genres = self.cleaned_data.get('genres')
        if not genres:
            raise ValidationError("At least one genre must be selected.")
        
        if len(genres) > 3:
            raise ValidationError("Maximum 3 genres can be selected. Choose your main styles.")
        
        return genres

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if not location:
            raise ValidationError("Location is required.")
        
        if len(location.strip()) < 3:
            raise ValidationError("Location must be at least 3 characters long.")
        
        return location.strip()

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Convert multi-select field values to comma-separated strings
        if self.cleaned_data.get('instruments_needed'):
            # Handle both predefined and custom values
            instrument_dict = dict(INSTRUMENT_CHOICES)
            instruments = []
            for inst in self.cleaned_data['instruments_needed']:
                # If it's a predefined choice, use the display value
                if inst in instrument_dict:
                    instruments.append(instrument_dict[inst])
                else:
                    # If it's a custom value, use it as-is (already formatted from frontend)
                    instruments.append(inst)
            instance.instruments_needed = ', '.join(instruments)
        
        if self.cleaned_data.get('genres'):
            # Handle both predefined and custom values
            genre_dict = dict(GENRE_CHOICES)
            genres = []
            for genre in self.cleaned_data['genres']:
                # If it's a predefined choice, use the display value
                if genre in genre_dict:
                    genres.append(genre_dict[genre])
                else:
                    # If it's a custom value, use it as-is (already formatted from frontend)
                    genres.append(genre)
            instance.genres = ', '.join(genres)
        
        if commit:
            instance.save()
        
        return instance