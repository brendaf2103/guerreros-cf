from django.contrib import messages
from django.shortcuts import redirect, render

from .models import (
    HeroSlide, Noticia, Logro, FotoCampeonas, GaleriaImagen,
    FilosofiaSlide, MaterialSlide, Patrocinador, EquipoFinalista, Publicidad,
    ValorFilosofia, EventoSlide, InfoCard,
    DatoEstadistico, VideoDestacado, InfoContacto, MensajeContacto,
)

# Orden fijo en el que se muestran los apartados de "Finales" en el sitio.
ORDEN_CATEGORIAS_FINALES = ["varonil_libre", "juvenil_mayor", "juvenil_menor", "femenil"]


def _agrupar_finalistas():
    """Agrupa EquipoFinalista por categoría, respetando el orden de la liga
    (Varonil Libre, Juvenil Mayor, Juvenil Menor, Femenil) y devuelve solo
    las categorías que ya tienen fotos cargadas."""
    todos = list(EquipoFinalista.objects.all())
    por_categoria = {cat: [] for cat in ORDEN_CATEGORIAS_FINALES}
    for item in todos:
        por_categoria.setdefault(item.categoria, []).append(item)
    secciones = []
    for cat in ORDEN_CATEGORIAS_FINALES:
        items = por_categoria.get(cat, [])
        if items:
            secciones.append({
                "clave": cat,
                "nombre": items[0].get_categoria_display(),
                "items": items,
            })
    return secciones


def index(request):
    noticias = Noticia.objects.all()
    contexto = {
        "hero_slides": HeroSlide.objects.all(),
        "estadisticas": DatoEstadistico.objects.all(),
        "noticia_principal": noticias.filter(destacada=True).first(),
        "noticias_secundarias": noticias.filter(destacada=False)[:3],
        "logros": Logro.objects.all(),
        "foto_campeonas_principal": FotoCampeonas.objects.filter(es_principal=True).first(),
        "fotos_campeonas_secundarias": FotoCampeonas.objects.filter(es_principal=False)[:2],
        # La galería completa puede tener cientos de fotos; se muestran las
        # primeras 90 en la carga inicial para que la página siga siendo rápida.
        "galeria": GaleriaImagen.objects.all()[:90],
        "total_galeria": GaleriaImagen.objects.count(),
        "filosofia_slides": FilosofiaSlide.objects.all(),
        "material_slides": MaterialSlide.objects.all(),
        "patrocinadores": Patrocinador.objects.all(),
        "finales_secciones": _agrupar_finalistas(),
        "publicidad": Publicidad.objects.all(),
        "valores": ValorFilosofia.objects.all(),
        "eventos": EventoSlide.objects.all(),
        "info_cards": InfoCard.objects.all(),
        "video": VideoDestacado.objects.first(),
        "contactos": InfoContacto.objects.all(),
        "categorias_form": [
            "Infantil (7–12 años)",
            "Juvenil Menor (13–15 años)",
            "Juvenil Mayor (16–18 años)",
            "Libre Varonil (+18)",
            "Libre Femenil (+18)",
        ],
    }
    return render(request, "core/index.html", contexto)


def enviar_mensaje(request):
    """Guarda el mensaje del formulario de contacto y regresa a la sección de contacto."""
    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        if nombre:
            MensajeContacto.objects.create(
                nombre=nombre,
                telefono=request.POST.get("telefono", "").strip(),
                categoria=request.POST.get("categoria", "").strip(),
                mensaje=request.POST.get("mensaje", "").strip(),
            )
            messages.success(request, "¡Gracias! Tu mensaje fue recibido, te contactaremos pronto.")
        else:
            messages.error(request, "Por favor ingresa tu nombre.")
    return redirect("/#contacto")
