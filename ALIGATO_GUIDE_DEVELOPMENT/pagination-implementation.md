# Listings Pagination Implementation

## Overview

The pagination feature limits the display of listings to 4 items per page, providing better user experience and performance for large datasets.

## Backend Implementation (views.py)

### Core Logic

```python
from django.core.paginator import Paginator

def listings_view(request):
    # Get base queryset with filters applied
    listings = Listing.objects.filter(is_active=True)

    # Apply search and filter logic
    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query) |
            Q(band_name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Order results
    listings = listings.order_by('-created_at')

    # Apply pagination
    paginator = Paginator(listings, 4)  # 4 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'listings': page_obj,  # Paginated listings
        'listings_count': paginator.count,  # Total count
        'page_obj': page_obj,  # Pagination controls
    }
```

### Key Changes Made

1. **Fixed pagination variable**: Changed `queryset` to `listings`
2. **Applied to both user types**: Musicians and band admins get pagination
3. **Preserved filters**: Search, genre, and instrument filters work with pagination

## Frontend Implementation (listings_feed.html)

### Pagination Controls Structure

```html
{% if page_obj.paginator.num_pages > 1 %}
<div class="flex justify-center mt-8">
  <nav class="flex items-center space-x-2">
    <!-- Previous Button -->
    {% if page_obj.has_previous %}
    <a href="?page={{ page_obj.previous_page_number }}&filters">
      <!-- Previous Icon -->
    </a>
    {% endif %}

    <!-- Page Numbers -->
    {% for num in page_obj.paginator.page_range %} {% if page_obj.number == num
    %}
    <span class="current-page">{{ num }}</span>
    {% else %}
    <a href="?page={{ num }}&filters">{{ num }}</a>
    {% endif %} {% endfor %}

    <!-- Next Button -->
    {% if page_obj.has_next %}
    <a href="?page={{ page_obj.next_page_number }}&filters">
      <!-- Next Icon -->
    </a>
    {% endif %}
  </nav>
</div>
{% endif %}
```

### Filter Preservation

The pagination URLs preserve GET parameters:

```html
href="?{% if current_filters.search %}search={{ current_filters.search }}&{%
endif %}{% if current_filters.genre %}genre={{ current_filters.genre }}&{% endif
%}{% if current_filters.instrument %}instrument={{ current_filters.instrument
}}&{% endif %}page={{ num }}"
```

## Visual Features

- **Current Page Highlight**: Active page shown with purple background
- **Disabled State**: Previous/Next buttons grayed out when unavailable
- **Page Range Limiting**: Shows pages within ±3 range of current page
- **Result Counter**: "Showing 1 to 4 of 15 results"

## Performance Benefits

1. **Reduced Load Time**: Only loads 4 listings at once
2. **Better UX**: Easier to browse through content
3. **Database Efficiency**: LIMIT/OFFSET queries reduce data transfer
4. **Mobile Friendly**: Less scrolling required

## Integration Points

- Works with search functionality
- Maintains filter states
- Compatible with both user types (musicians/band admins)
- Preserves recent applications display within each listing card
