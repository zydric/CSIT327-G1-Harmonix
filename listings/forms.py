from django import forms
from django.core.exceptions import ValidationError
from .models import Listing
from harmonix.constants import GENRE_CHOICES, INSTRUMENT_CHOICES


class ListingForm(forms.ModelForm):
    """
    Form for creating and editing band listings
    """
    # Override fields to use multi-select widgets
    instruments_needed = forms.MultipleChoiceField(
        choices=INSTRUMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'space-y-2'
        }),
        help_text="Select all instruments needed for this opportunity"
    )
    
    genres = forms.MultipleChoiceField(
        choices=GENRE_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'space-y-2'
        }),
        help_text="Select all genres that describe your band's style"
    )

    class Meta:
        model = Listing
        fields = ['title', 'band_name', 'description', 'instruments_needed', 'genres', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'e.g., "Lead Guitarist Needed for Rock Band"'
            }),
            'band_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Your band name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'rows': 6,
                'placeholder': 'Describe the opportunity, requirements, and what you\'re looking for in detail...'
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
        
        return title.strip()

    def clean_band_name(self):
        band_name = self.cleaned_data.get('band_name')
        if not band_name:
            raise ValidationError("Band name is required.")
        
        if len(band_name.strip()) < 2:
            raise ValidationError("Band name must be at least 2 characters long.")
        
        return band_name.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise ValidationError("Description is required.")
        
        if len(description.strip()) < 50:
            raise ValidationError("Description must be at least 50 characters long to provide enough detail.")
        
        return description.strip()

    def clean_instruments_needed(self):
        instruments = self.cleaned_data.get('instruments_needed')
        if not instruments:
            raise ValidationError("At least one instrument must be selected.")
        
        if len(instruments) > 5:
            raise ValidationError("Maximum 5 instruments can be selected.")
        
        return instruments

    def clean_genres(self):
        genres = self.cleaned_data.get('genres')
        if not genres:
            raise ValidationError("At least one genre must be selected.")
        
        if len(genres) > 4:
            raise ValidationError("Maximum 4 genres can be selected.")
        
        return genres

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Convert multi-select field values to comma-separated strings
        if self.cleaned_data.get('instruments_needed'):
            # Convert to display values (capitalized)
            instrument_dict = dict(INSTRUMENT_CHOICES)
            instruments = [
                instrument_dict.get(inst, inst.capitalize()) 
                for inst in self.cleaned_data['instruments_needed']
            ]
            instance.instruments_needed = ', '.join(instruments)
        
        if self.cleaned_data.get('genres'):
            # Convert to display values (capitalized)
            genre_dict = dict(GENRE_CHOICES)
            genres = [
                genre_dict.get(genre, genre.capitalize()) 
                for genre in self.cleaned_data['genres']
            ]
            instance.genres = ', '.join(genres)
        
        if commit:
            instance.save()
        
        return instance