from django.contrib import admin

from models import Event
from vikiticket.core.models import Row, Placement, Stage, Order, Tag, \
    PriceCategory, UserProfile, Seat, Client, Page


class PageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'ordering')
    exclude = ('event',)
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.event = request.user.profile.event
        obj.save()

    def queryset(self, request):
        qs = super(PageAdmin, self).queryset(request)
        return qs.filter(event=request.user.profile.event)

admin.site.register(Page, PageAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'performer', 'bottom_info', 'date', 'is_published')
    save_on_top = True

    def queryset(self, request):
        qs = super(EventAdmin, self).queryset(request)
        return qs.filter(pk=request.user.profile.event.pk)

admin.site.register(Event, EventAdmin)


class SeatInline(admin.TabularInline):
    model = Seat
    exclude = ('event',)
    readonly_fields = ('number',)
    fields = ('number', 'status', 'price_category', 'order', 'tag', 'comment')
    extra = 0
    max_num = 0
    can_delete = False

    def queryset(self, request):
        qs = super(SeatInline, self).queryset(request)
        return qs.filter(event=request.user.profile.event)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'order':
            kwargs['queryset'] = Order.objects.filter(event=request.user.profile.event)
        if db_field.name == 'price_category':
            kwargs['queryset'] = PriceCategory.objects.filter(event=request.user.profile.event)
        if db_field.name == 'tag':
            kwargs['queryset'] = Tag.objects.filter(event=request.user.profile.event)
        return super(SeatInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class SeatInlineForOrder(SeatInline):
    readonly_fields = ('number', 'status', 'price_category', 'order', 'tag', 'comment')


class RowAdmin(admin.ModelAdmin):
    inlines = [SeatInline]
    list_display = ('number', 'placement', 'seat_count')
    list_display_links = ('placement', 'number')
    exclude = ('event',)
    readonly_fields = ('placement', 'number')
    ordering = ('number', 'placement')
#    list_filter = ('placement',)
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.event = request.user.profile.event
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.event = request.user.profile.event
            instance.save()
        formset.save_m2m()

    def queryset(self, request):
        qs = super(RowAdmin, self).queryset(request)
        return qs.filter(event=request.user.profile.event)

admin.site.register(Row, RowAdmin)


class RowInline(admin.TabularInline):
    model = Row
    inlines = [Seat]
    exclude = ('event',)
    extra = 0
    max_num = 0
    can_delete = False

    def queryset(self, request):
        qs = super(RowInline, self).queryset(request)
        return qs.filter(event=request.user.profile.event)


class PlacementAdmin(admin.ModelAdmin):
    inlines = [RowInline]
    list_display = ('name', 'stage')
    exclude = ('event',)
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.event = request.user.profile.event
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.event = request.user.profile.event
            instance.save()
        formset.save_m2m()

    def queryset(self, request):
        qs = super(PlacementAdmin, self).queryset(request)
        return qs.filter(event=request.user.profile.event)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'stage':
            kwargs['queryset'] = Stage.objects.filter(event=request.user.profile.event)
        return super(PlacementAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Placement, PlacementAdmin)


class PlacementInline(admin.TabularInline):
    model = Placement
    inlines = [Row]
    exclude = ('event',)
    extra = 0
    can_delete = False

    def queryset(self, request):
        qs = super(PlacementInline, self).queryset(request)
        return qs.filter(event=request.user.profile.event)


class StageAdmin(admin.ModelAdmin):
    inlines = [PlacementInline]
    list_display = ('name',)
    exclude = ('event',)
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.event = request.user.profile.event
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.event = request.user.profile.event
            instance.save()
        formset.save_m2m()

    def queryset(self, request):
        qs = super(StageAdmin, self).queryset(request)
        return qs.filter(event=request.user.profile.event)

admin.site.register(Stage, StageAdmin)


class OrderInline(admin.TabularInline):
    model = Order
    exclude = ('event',)
    extra = 0
    readonly_fields = ('close_date',)

    def queryset(self, request):
        qs = super(OrderInline, self).queryset(request)
        return qs.filter(event=request.user.profile.event)

class ClientAdmin(admin.ModelAdmin):
    inlines = [OrderInline]
    list_fields = ('name', 'phone', 'email')
    exclude = ('event',)
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.event = request.user.profile.event
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.event = request.user.profile.event
            instance.save()
        formset.save_m2m()

    def queryset(self, request):
        qs = super(ClientAdmin, self).queryset(request)
        return qs.filter(event=request.user.profile.event)

admin.site.register(Client, ClientAdmin)


class OrderAdmin(admin.ModelAdmin):
    inlines = [SeatInlineForOrder]
    list_display = ('client', 'id', 'create_date', 'status', 'total_price', 'update_date', 'close_date')
    list_display_links = ('id', 'client')
    readonly_fields = ('close_date',)
    exclude = ('event',)
    list_filter = ('status',) # 'client')
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.event = request.user.profile.event
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.event = request.user.profile.event
            instance.save()
        formset.save_m2m()

    def queryset(self, request):
        qs = super(OrderAdmin, self).queryset(request)
        return qs.filter(event=request.user.profile.event)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'client':
            kwargs['queryset'] = Client.objects.filter(event=request.user.profile.event)
        return super(OrderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Order, OrderAdmin)


class SeatAdmin(admin.ModelAdmin):
    list_display = ('row', 'colored_number', 'status', 'order_pretty', 'price_category', 'comment', 'tag')
    readonly_fields = ('number', 'row')
    list_display_links = ('colored_number', 'row',)
    exclude = ('event',)
    readonly_fields = ('row', 'number')
    ordering = ('row', 'number',)
    list_filter = ('status',) #'price_category', 'tag', 'row', 'order', 'comment')
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.event = request.user.profile.event
        obj.save()

    def queryset(self, request):
        qs = super(SeatAdmin, self).queryset(request)
        return qs.filter(event=request.user.profile.event)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'order':
            kwargs['queryset'] = Order.objects.filter(event=request.user.profile.event)
        if db_field.name == 'price_category':
            kwargs['queryset'] = PriceCategory.objects.filter(event=request.user.profile.event)
        if db_field.name == 'tag':
            kwargs['queryset'] = Tag.objects.filter(event=request.user.profile.event)
        return super(SeatAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Seat, SeatAdmin)


class TagAdmin(admin.ModelAdmin):
    inlines = [SeatInline]
    list_display = ('name', 'color', 'create_date')
    exclude = ('event',)
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.event = request.user.profile.event
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.event = request.user.profile.event
            instance.save()
        formset.save_m2m()

    def queryset(self, request):
        qs = super(TagAdmin, self).queryset(request)
        return qs.filter(event=request.user.profile.event)

admin.site.register(Tag, TagAdmin)


class PriceCategoryAdmin(admin.ModelAdmin):
    inlines = [SeatInline]
    list_display = ('color', 'price')
    exclude = ('event',)
    save_on_top = True

    def save_model(self, request, obj, form, change):
        obj.event = request.user.profile.event
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.event = request.user.profile.event
            instance.save()
        formset.save_m2m()

    def queryset(self, request):
        qs = super(PriceCategoryAdmin, self).queryset(request)
        return qs.filter(event=request.user.profile.event)

admin.site.register(PriceCategory, PriceCategoryAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')

admin.site.register(UserProfile, UserProfileAdmin)
