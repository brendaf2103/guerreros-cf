from django.db import models


class HeroSlide(models.Model):
    """Fotos grandes del carrusel principal (Inicio)."""
    imagen = models.ImageField("Imagen", upload_to="img/")
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Foto del Inicio (Hero)"
        verbose_name_plural = "1. Inicio — Carrusel principal"
        ordering = ["orden", "id"]

    def __str__(self):
        return f"Hero #{self.orden} — {self.imagen.name}"


class Noticia(models.Model):
    """Sección de Noticias."""
    titulo = models.CharField("Título", max_length=200)
    categoria = models.CharField("Categoría", max_length=60, help_text="Ej: 🏆 Torneo Nacional")
    resumen = models.TextField("Resumen / Descripción")
    fecha_texto = models.CharField("Fecha (texto libre)", max_length=40, default="2026")
    imagen = models.ImageField("Imagen", upload_to="img/")
    destacada = models.BooleanField("¿Es la noticia principal?", default=False)
    enlace_seccion = models.CharField(
        "Enlace interno", max_length=50, default="academia",
        help_text="A qué sección del sitio enlaza esta tarjeta (sin #), ej: academia, campeonas, galeria",
    )
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "2. Noticias"
        ordering = ["-destacada", "orden", "-id"]

    def __str__(self):
        return self.titulo


class Logro(models.Model):
    """Logros / palmarés que se muestran en la sección Campeonas."""
    icono = models.CharField("Icono (emoji)", max_length=10, default="🏆")
    titulo = models.CharField("Título", max_length=150)
    descripcion = models.CharField("Descripción", max_length=200)
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Logro"
        verbose_name_plural = "3. Campeonas — Logros"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.titulo


class FotoCampeonas(models.Model):
    """Fotos de la sección Campeonas (una principal + dos pequeñas)."""
    imagen = models.ImageField("Imagen", upload_to="img/")
    es_principal = models.BooleanField("¿Es la foto grande?", default=False)
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Foto de Campeonas"
        verbose_name_plural = "3. Campeonas — Fotos"
        ordering = ["-es_principal", "orden", "id"]

    def __str__(self):
        return f"Foto Campeonas #{self.orden}"


class GaleriaImagen(models.Model):
    """Galería general de fotos del equipo (más de 250 fotos)."""
    imagen = models.ImageField("Imagen", upload_to="img/")
    titulo = models.CharField("Título (opcional)", max_length=120, blank=True)
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Foto de Galería"
        verbose_name_plural = "4. Galería"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.titulo or f"Galería #{self.orden}"


class EquipoFinalista(models.Model):
    """Fotos de campeones, subcampeones y premios individuales de cada categoría."""
    CATEGORIA_CHOICES = [
        ("varonil_libre", "Varonil Libre"),
        ("juvenil_mayor", "Juvenil Mayor"),
        ("juvenil_menor", "Juvenil Menor"),
        ("femenil", "Femenil"),
    ]
    TIPO_CHOICES = [
        ("liga_1", "🥇 Liga — 1er lugar"),
        ("liga_2", "🥈 Liga — 2do lugar"),
        ("copa_1", "🥇 Copa — 1er lugar"),
        ("copa_2", "🥈 Copa — 2do lugar"),
        ("consolacion_2", "🥈 Consolación — 2do lugar"),
        ("primer_lugar", "🥇 1er lugar"),
        ("segundo_lugar", "🥈 2do lugar"),
        ("mejor_portero", "🧤 Mejor Portero"),
        ("mejor_goleador", "⚽ Mejor Goleador"),
    ]
    imagen = models.ImageField("Imagen", upload_to="img/")
    categoria = models.CharField("Categoría", max_length=20, choices=CATEGORIA_CHOICES)
    tipo = models.CharField("Premio / lugar", max_length=20, choices=TIPO_CHOICES)
    equipo = models.CharField("Nombre del equipo o jugador (opcional)", max_length=100, blank=True)
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Equipo / Premio Finalista"
        verbose_name_plural = "5d. Finales de Torneo — Equipos y Premios"
        ordering = ["categoria", "orden", "id"]

    def __str__(self):
        return f"{self.get_categoria_display()} — {self.get_tipo_display()}"


class Publicidad(models.Model):
    """Flyers y anuncios promocionales de la academia (convocatorias, torneos, etc.)."""
    imagen = models.ImageField("Imagen", upload_to="img/")
    titulo = models.CharField("Título (opcional)", max_length=120, blank=True)
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Publicidad"
        verbose_name_plural = "5e. Publicidad — Flyers y Anuncios"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.titulo or f"Publicidad #{self.orden}"


class FilosofiaSlide(models.Model):
    """Láminas del carrusel de la sección Filosofía (filo1–filo11)."""
    imagen = models.ImageField("Imagen", upload_to="img/")
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Foto de Filosofía"
        verbose_name_plural = "5. Filosofía — Carrusel"
        ordering = ["orden", "id"]

    def __str__(self):
        return f"Filosofía #{self.orden}"


class MaterialSlide(models.Model):
    """Láminas del carrusel de Materiales de Entrenamiento (filo12–filo26)."""
    imagen = models.ImageField("Imagen", upload_to="img/")
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Foto de Material de Entrenamiento"
        verbose_name_plural = "5b. Materiales de Entrenamiento — Carrusel"
        ordering = ["orden", "id"]

    def __str__(self):
        return f"Material #{self.orden}"


class Patrocinador(models.Model):
    """Franja de logos de patrocinadores/instituciones que apoyan al equipo."""
    imagen = models.ImageField(
        "Imagen (franja de logos o logo individual)", upload_to="img/",
        help_text="Puede ser una sola imagen con todos los logos, o subir varias filas.",
    )
    nombre = models.CharField("Nombre (opcional)", max_length=100, blank=True)
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Patrocinador"
        verbose_name_plural = "5c. Patrocinadores"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.nombre or f"Patrocinador #{self.orden}"


class ValorFilosofia(models.Model):
    """Lista de valores mostrados junto al carrusel de filosofía."""
    icono = models.CharField("Icono (emoji)", max_length=10, default="⚽")
    texto = models.CharField("Texto", max_length=150)
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Valor"
        verbose_name_plural = "5. Filosofía — Valores"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.texto


class EventoSlide(models.Model):
    """Carrusel grande de Eventos con miniaturas."""
    imagen = models.ImageField("Imagen", upload_to="img/")
    badge = models.CharField("Etiqueta (emoji + texto)", max_length=60)
    titulo = models.CharField("Título", max_length=150)
    descripcion = models.CharField("Descripción", max_length=220)
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "6. Eventos"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.titulo


class InfoCard(models.Model):
    """Tarjetas informativas de la sección Academia (horarios, categorías, etc.)."""
    icono = models.CharField("Icono (emoji)", max_length=10, default="⚽")
    titulo = models.CharField("Título", max_length=100)
    contenido_html = models.TextField(
        "Contenido (admite <br/> y <strong>)",
        help_text="Se inserta tal cual dentro de la tarjeta, puedes usar <br/> y <strong>.",
    )
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Tarjeta de la Academia"
        verbose_name_plural = "7. Academia — Tarjetas"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.titulo


class DatoEstadistico(models.Model):
    """Los números grandes de la barra de estadísticas (3 divisiones, 120+ jugadores...)."""
    numero = models.CharField("Número / símbolo", max_length=20)
    etiqueta = models.CharField("Etiqueta", max_length=60)
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Estadística"
        verbose_name_plural = "8. Estadísticas"
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.numero} — {self.etiqueta}"


class VideoDestacado(models.Model):
    """Video(s) destacados de la academia (resumen / highlights).

    Puedes usar CUALQUIERA de las dos opciones:
    - youtube_url: pega el link de un video ya subido a YouTube (recomendado
      para videos pesados — YouTube no tiene límite de tamaño y es gratis).
    - video: sube el archivo directamente (solo recomendado para clips
      cortos, ya que Cloudinary gratis tiene un límite de 100 MB por video).
    Si llenas youtube_url, el sitio lo muestra a él en vez del archivo.
    """
    titulo = models.CharField("Título", max_length=150, default="Guerreros CF en acción")
    descripcion = models.CharField("Descripción", max_length=250, blank=True)
    youtube_url = models.URLField(
        "Link de YouTube (recomendado)", blank=True,
        help_text="Pega aquí el link del video ya subido a YouTube, ej: https://www.youtube.com/watch?v=XXXXXXXXXXX",
    )
    video = models.FileField(
        "Archivo de video (alternativa, solo clips cortos < 100 MB)",
        upload_to="videos/", blank=True, null=True,
    )
    portada = models.ImageField("Imagen de portada (opcional)", upload_to="img/", blank=True, null=True)
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "9. Video destacado"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.titulo

    @property
    def youtube_embed_url(self):
        """Convierte cualquier formato de link de YouTube en un link de embed."""
        url = self.youtube_url or ""
        video_id = ""
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1].split("?")[0]
        elif "watch?v=" in url:
            video_id = url.split("watch?v=")[-1].split("&")[0]
        elif "/embed/" in url:
            video_id = url.split("/embed/")[-1].split("?")[0]
        elif "/shorts/" in url:
            video_id = url.split("/shorts/")[-1].split("?")[0]
        return f"https://www.youtube.com/embed/{video_id}" if video_id else ""


class InfoContacto(models.Model):
    """Datos de contacto configurables (teléfono, ubicación, horario...)."""
    icono = models.CharField("Icono (emoji)", max_length=10, default="📱")
    titulo = models.CharField("Título", max_length=100)
    detalle = models.CharField("Detalle", max_length=200)
    orden = models.PositiveIntegerField("Orden", default=0)

    class Meta:
        verbose_name = "Dato de contacto"
        verbose_name_plural = "10. Contacto"
        ordering = ["orden", "id"]

    def __str__(self):
        return self.titulo


class MensajeContacto(models.Model):
    """Mensajes que dejan los visitantes desde el formulario de contacto."""
    nombre = models.CharField("Nombre completo", max_length=120)
    telefono = models.CharField("WhatsApp / Teléfono", max_length=30, blank=True)
    categoria = models.CharField("Categoría de interés", max_length=60, blank=True)
    mensaje = models.TextField("Mensaje", blank=True)
    creado = models.DateTimeField("Recibido", auto_now_add=True)

    class Meta:
        verbose_name = "Mensaje recibido"
        verbose_name_plural = "11. Mensajes de contacto"
        ordering = ["-creado"]

    def __str__(self):
        return f"{self.nombre} ({self.creado:%d/%m/%Y})"
