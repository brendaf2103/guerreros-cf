from django.contrib import admin
from django.utils.html import format_html

from .models import (
    HeroSlide, Noticia, Logro, FotoCampeonas, GaleriaImagen,
    FilosofiaSlide, MaterialSlide, Patrocinador, EquipoFinalista, Publicidad,
    ValorFilosofia, EventoSlide, InfoCard,
    DatoEstadistico, VideoDestacado, InfoContacto, MensajeContacto,
)


class ThumbAdminMixin:
    """Muestra una miniatura de la imagen en la lista del admin."""
    image_field = "imagen"

    def miniatura(self, obj):
        img = getattr(obj, self.image_field, None)
        if img:
            return format_html('<img src="{}" style="height:60px;border-radius:6px" />', img.url)
        return "—"
    miniatura.short_description = "Vista previa"


@admin.register(HeroSlide)
class HeroSlideAdmin(ThumbAdminMixin, admin.ModelAdmin):
    list_display = ("miniatura", "orden", "imagen")
    list_editable = ("orden",)


@admin.register(Noticia)
class NoticiaAdmin(ThumbAdminMixin, admin.ModelAdmin):
    list_display = ("miniatura", "titulo", "categoria", "destacada", "orden")
    list_editable = ("orden",)
    list_filter = ("destacada",)
    search_fields = ("titulo", "resumen")


@admin.register(Logro)
class LogroAdmin(admin.ModelAdmin):
    list_display = ("icono", "titulo", "descripcion", "orden")
    list_editable = ("orden",)


@admin.register(FotoCampeonas)
class FotoCampeonasAdmin(ThumbAdminMixin, admin.ModelAdmin):
    list_display = ("miniatura", "es_principal", "orden")
    list_editable = ("orden",)


@admin.register(GaleriaImagen)
class GaleriaImagenAdmin(ThumbAdminMixin, admin.ModelAdmin):
    list_display = ("miniatura", "titulo", "orden")
    list_editable = ("orden",)
    search_fields = ("titulo",)


@admin.register(FilosofiaSlide)
class FilosofiaSlideAdmin(ThumbAdminMixin, admin.ModelAdmin):
    list_display = ("miniatura", "orden")
    list_editable = ("orden",)


@admin.register(MaterialSlide)
class MaterialSlideAdmin(ThumbAdminMixin, admin.ModelAdmin):
    list_display = ("miniatura", "orden")
    list_editable = ("orden",)


@admin.register(Patrocinador)
class PatrocinadorAdmin(ThumbAdminMixin, admin.ModelAdmin):
    list_display = ("miniatura", "nombre", "orden")
    list_editable = ("orden",)


@admin.register(EquipoFinalista)
class EquipoFinalistaAdmin(ThumbAdminMixin, admin.ModelAdmin):
    list_display = ("miniatura", "categoria", "tipo", "equipo", "orden")
    list_editable = ("orden",)
    list_filter = ("categoria", "tipo")


@admin.register(Publicidad)
class PublicidadAdmin(ThumbAdminMixin, admin.ModelAdmin):
    list_display = ("miniatura", "titulo", "orden")
    list_editable = ("orden",)


@admin.register(ValorFilosofia)
class ValorFilosofiaAdmin(admin.ModelAdmin):
    list_display = ("icono", "texto", "orden")
    list_editable = ("orden",)


@admin.register(EventoSlide)
class EventoSlideAdmin(ThumbAdminMixin, admin.ModelAdmin):
    list_display = ("miniatura", "titulo", "badge", "orden")
    list_editable = ("orden",)


@admin.register(InfoCard)
class InfoCardAdmin(admin.ModelAdmin):
    list_display = ("icono", "titulo", "orden")
    list_editable = ("orden",)


@admin.register(DatoEstadistico)
class DatoEstadisticoAdmin(admin.ModelAdmin):
    list_display = ("numero", "etiqueta", "orden")
    list_editable = ("orden",)


@admin.register(VideoDestacado)
class VideoDestacadoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "youtube_url", "video", "orden")
    list_editable = ("orden",)


@admin.register(InfoContacto)
class InfoContactoAdmin(admin.ModelAdmin):
    list_display = ("icono", "titulo", "detalle", "orden")
    list_editable = ("orden",)


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono", "categoria", "creado")
    readonly_fields = ("creado",)
    list_filter = ("categoria",)
    search_fields = ("nombre", "telefono", "mensaje")


admin.site.site_header = "Academia Guerreros CF Yauhquemehcan"
admin.site.site_title = "Panel Guerreros CF"
admin.site.index_title = "Administración del sitio"
