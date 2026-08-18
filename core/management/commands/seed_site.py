"""
Comando de administración que llena la base de datos con todo el contenido
del sitio (portada, noticias, campeonas, galería, filosofía, eventos,
academia, estadísticas, video y contacto) usando las imágenes que ya están
copiadas en media/img/ y media/videos/.

Uso:
    python manage.py seed_site
"""
from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import (
    HeroSlide, Noticia, Logro, FotoCampeonas, GaleriaImagen,
    FilosofiaSlide, MaterialSlide, Patrocinador, EquipoFinalista, Publicidad,
    ValorFilosofia, EventoSlide, InfoCard,
    DatoEstadistico, VideoDestacado, InfoContacto,
)


class Command(BaseCommand):
    help = "Llena el sitio con el contenido inicial de la Academia Guerreros CF"

    def handle(self, *args, **options):
        img_dir = settings.MEDIA_ROOT / "img"
        if not img_dir.exists():
            self.stderr.write(self.style.ERROR(
                f"No se encontró la carpeta {img_dir}. Copia primero las imágenes a media/img/."
            ))
            return

        self.stdout.write("Limpiando contenido anterior...")
        for Model in (HeroSlide, Noticia, Logro, FotoCampeonas, GaleriaImagen,
                      FilosofiaSlide, MaterialSlide, Patrocinador, EquipoFinalista, Publicidad,
                      ValorFilosofia, EventoSlide, InfoCard,
                      DatoEstadistico, VideoDestacado, InfoContacto):
            Model.objects.all().delete()

        # ── 1. HERO (Inicio) ──
        hero_imgs = ["1.jpg", "5.jpg", "10.jpg", "15.jpg", "20.jpg", "25.jpg",
                     "Guerreras.jpg", "707378315_1357056453145990_8240587692205455897_n.jpg"]
        for i, name in enumerate(hero_imgs):
            self._create_img(HeroSlide, name, orden=i)

        # ── 8. ESTADÍSTICAS ──
        for i, (num, lbl) in enumerate([
            ("3", "Divisiones"),
            ("120+", "Jugadores"),
            ("7+", "Años de historia"),
            ("🏆", "Campeones Nacionales"),
        ]):
            DatoEstadistico.objects.create(numero=num, etiqueta=lbl, orden=i)

        # ── 2. NOTICIAS ──
        Noticia.objects.create(
            titulo="¡Guerreras CF Campeonas del Nacional FMF7!",
            categoria="🏆 Torneo Nacional",
            resumen=("El equipo femenil de Guerreros CF Yauhquemehcan se coronó campeón "
                      "nacional en la Federación Mexicana de Fútbol 7, representando con "
                      "orgullo a Tlaxcala ante todo el país."),
            fecha_texto="2026",
            imagen=self._rel("707378315_1357056453145990_8240587692205455897_n.jpg"),
            destacada=True,
            enlace_seccion="campeonas",
            orden=0,
        )
        noticias_sec = [
            dict(titulo="Guerreras CF conquistan el primer lugar en torneo estatal FMF7",
                 categoria="🥇 Femenil", fecha_texto="Mayo 2026", imagen="Guerreras.jpg",
                 enlace_seccion="campeonas"),
            dict(titulo="Inscripciones abiertas: niños, niñas y jóvenes de 7 a 18 años",
                 categoria="⚽ Academia", fecha_texto="2026", imagen="foto1.jpg",
                 enlace_seccion="academia"),
            dict(titulo="Participación en torneos estatales, regionales y nacionales",
                 categoria="🎖️ Logros", fecha_texto="Temporada 2026", imagen="evento1.jpg",
                 enlace_seccion="galeria"),
            dict(titulo="Liga Varonil Libre y Femenil Libre todos los domingos",
                 categoria="🛡️ Liga", fecha_texto="Temporada 2026",
                 imagen="707816140_1357048886480080_9658495399272881_n.jpg",
                 enlace_seccion="academia"),
        ]
        for i, n in enumerate(noticias_sec):
            Noticia.objects.create(
                titulo=n["titulo"], categoria=n["categoria"], resumen="",
                fecha_texto=n["fecha_texto"], imagen=self._rel(n["imagen"]),
                destacada=False, enlace_seccion=n["enlace_seccion"], orden=i,
            )

        # ── 3. CAMPEONAS ──
        for i, (icono, titulo, desc) in enumerate([
            ("🏆", "Campeonas del Nacional FMF7", "Federación Mexicana de Fútbol 7 — 2026"),
            ("🥇", "Primer lugar estatal Tlaxcala", "Torneo estatal femenil libre — 2025/2026"),
            ("🎖️", "Torneos regionales y estatales", "Múltiples participaciones y títulos obtenidos"),
            ("💪", "Disciplina · Respeto · Pasión", "Los valores que forman a nuestras guerreras"),
        ]):
            Logro.objects.create(icono=icono, titulo=titulo, descripcion=desc, orden=i)

        self._create_img(FotoCampeonas, "Guerreras.jpg", es_principal=True, orden=0)
        self._create_img(FotoCampeonas, "707378315_1357056453145990_8240587692205455897_n.jpg",
                          es_principal=False, orden=1)
        self._create_img(FotoCampeonas, "707816140_1357048886480080_9658495399272881_n.jpg",
                          es_principal=False, orden=2)

        # ── 4. GALERÍA (fotos numeradas 1–190 + fotos especiales) ──
        orden = 0
        for i in range(1, 191):
            name = f"{i}.jpg"
            if (img_dir / name).exists():
                self._create_img(GaleriaImagen, name, orden=orden)
                orden += 1
        especiales = [
            "Guerreras.jpg", "foto1.jpg", "foto5.jpg",
            "evento1.jpg", "evento2.jpg", "evento3.jpg", "evento4.jpg", "evento5.jpg",
            "evento6.jpg", "evento7.jpg", "evento8.jpg", "evento9.jpg",
            "mave.jpg", "uniformes.jpg", "entrenamientos.jpg",
        ]
        # Todas las fotos descargadas de Facebook / WhatsApp también entran a galería
        extra_fb = sorted(p.name for p in img_dir.glob("7*_n.jpg"))
        extra_wa = sorted(p.name for p in img_dir.glob("WhatsApp Image*"))
        for name in especiales + extra_fb + extra_wa:
            if (img_dir / name).exists():
                self._create_img(GaleriaImagen, name, orden=orden)
                orden += 1

        # ── 5. FILOSOFÍA (filo1–filo11: láminas de la filosofía de la academia) ──
        for i in range(1, 12):
            name = f"filo{i}.jpg"
            if (img_dir / name).exists():
                self._create_img(FilosofiaSlide, name, orden=i - 1)

        # ── 5b. MATERIALES DE ENTRENAMIENTO (filo12–filo26: guía de equipo) ──
        for i in range(12, 27):
            name = f"filo{i}.jpg"
            if (img_dir / name).exists():
                self._create_img(MaterialSlide, name, orden=i - 12)

        # ── 5c. PATROCINADORES (franja de logos recortada de mave.jpg) ──
        if (img_dir / "patrocinadores.jpg").exists():
            self._create_img(Patrocinador, "patrocinadores.jpg", nombre="Instituciones y patrocinadores", orden=0)

        # ── 5d. FINALES DE TORNEO (equipos campeones y subcampeones) ──
        finalistas = [
            # ── Varonil Libre ──
            ("final_liga_1.jpg", "varonil_libre", "liga_1", "Golden Team"),
            ("final_liga_2.jpg", "varonil_libre", "liga_2", "Selección México"),
            ("final_copa_1.jpg", "varonil_libre", "copa_1", "Bayern"),
            ("final_copa_2.jpg", "varonil_libre", "copa_2", ""),
            ("final_consolacion_2.jpg", "varonil_libre", "consolacion_2", ""),
            ("final_vl_portero.jpg", "varonil_libre", "mejor_portero", ""),
            ("final_vl_goleador.jpg", "varonil_libre", "mejor_goleador", ""),
            # ── Juvenil Mayor ──
            ("final_jmayor_1.jpg", "juvenil_mayor", "primer_lugar", "Tigres"),
            ("final_jmayor_2.jpg", "juvenil_mayor", "segundo_lugar", ""),
            ("final_jmayor_goleador.jpg", "juvenil_mayor", "mejor_goleador", ""),
            ("final_jmayor_portero.jpg", "juvenil_mayor", "mejor_portero", ""),
            # ── Juvenil Menor ──
            ("final_jmenor_1.jpg", "juvenil_menor", "primer_lugar", ""),
            ("final_jmenor_2.jpg", "juvenil_menor", "segundo_lugar", ""),
            ("final_jmenor_goleador.jpg", "juvenil_menor", "mejor_goleador", ""),
            ("final_jmenor_portero.jpg", "juvenil_menor", "mejor_portero", ""),
        ]
        for i, (name, categoria, tipo, equipo) in enumerate(finalistas):
            if (img_dir / name).exists():
                self._create_img(EquipoFinalista, name, categoria=categoria, tipo=tipo, equipo=equipo, orden=i)

        # ── 5e. PUBLICIDAD (flyers y anuncios de convocatorias/torneos) ──
        for i in range(1, 40):
            name = f"pub{i}.jpg"
            if (img_dir / name).exists():
                self._create_img(Publicidad, name, orden=i - 1)

        for i, (icono, texto) in enumerate([
            ("⚽", "Entrenamientos grupales y personalizados"),
            ("🏃", "Categorías infantil, juvenil y libre"),
            ("👩‍⚽", "Liga Femenil y Varonil todos los domingos"),
            ("🏆", "Participación en torneos estatales y nacionales"),
            ("❤️", "Disciplina · Respeto · Esfuerzo · Trabajo en equipo"),
        ]):
            ValorFilosofia.objects.create(icono=icono, texto=texto, orden=i)

        # ── 6. EVENTOS ──
        eventos = [
            ("evento1.jpg", "🏆 Torneo Nacional", "Campeonato Nacional FMF7",
             "Las Guerreras CF conquistan el título nacional representando a Tlaxcala"),
            ("evento2.jpg", "⚽ Liga Dominical", "Liga Varonil y Femenil Libre",
             "Competencia semanal todos los domingos en la Unidad Deportiva"),
            ("evento3.jpg", "🎖️ Reconocimiento", "Estrategia Nacional de Turismo Deportivo Tlaxcala 2026",
             "La academia presente en eventos deportivos de alto impacto regional"),
            ("evento4.jpg", "🏃 Entrenamiento", "Entrenamientos de Alto Rendimiento",
             "Formación integral: técnica, física y táctica para todas las categorías"),
            ("evento5.jpg", "👧 Femenil", "Equipo Femenil en Acción",
             "Las Guerreras demuestran su nivel en cada cancha que pisan"),
            ("evento6.jpg", "🌟 Torneo Estatal", "Torneos Estatales Tlaxcala",
             "Representando a Yauhquemehcan con orgullo en cada torneo"),
            ("evento7.jpg", "🥇 Logros", "Trofeos y Reconocimientos",
             "El resultado del esfuerzo, la disciplina y el trabajo en equipo"),
            ("evento8.jpg", "⚽ Academia", "Academia Guerreros CF Yauhquemehcan",
             "Formando campeones dentro y fuera de la cancha desde San Dionisio"),
            ("evento9.jpg", "🎽 Juvenil", "Categoría Juvenil",
             "Juvenil Menor y Juvenil Mayor: el futuro de la academia"),
        ]
        for i, (img, badge, titulo, desc) in enumerate(eventos):
            EventoSlide.objects.create(
                imagen=self._rel(img), badge=badge, titulo=titulo, descripcion=desc, orden=i,
            )

        # ── 7. ACADEMIA (tarjetas de información) ──
        info = [
            ("🕐", "Horarios",
             "Entrenamientos <strong>Lunes, Miércoles y Viernes</strong><br/>de 4:00 a 6:00 PM"
             "<br/><br/>Liga Dominical todos los <strong>domingos</strong>"),
            ("👥", "Categorías",
             "<strong>Infantil y Juvenil:</strong> niños, niñas y jóvenes de 7 a 18 años"
             "<br/><br/><strong>Categoría Libre:</strong> mayores de 18 años — Varonil y Femenil"),
            ("📍", "Ubicación",
             "<strong>San Dionisio Yauhquemehcan</strong><br/>Unidad Deportiva<br/>Tlaxcala, México"
             "<br/><br/>Contáctanos al <strong>241-105-5982</strong>"),
            ("⚽", "Entrenamientos",
             "Grupales y personalizados.<br/><strong>Mixtos</strong> para todas las edades y niveles. "
             "Técnica, táctica y preparación física integral."),
            ("🏆", "Competencias",
             "Participamos en torneos <strong>estatales, regionales y nacionales</strong>."
             "<br/>Campeones nacionales FMF7 2026."),
            ("❤️", "Valores",
             "<strong>Disciplina · Respeto<br/>Esfuerzo · Trabajo en equipo</strong>"
             "<br/><br/>Formamos jugadores y personas de bien."),
        ]
        for i, (icono, titulo, contenido) in enumerate(info):
            InfoCard.objects.create(icono=icono, titulo=titulo, contenido_html=contenido, orden=i)

        # ── 9. VIDEO DESTACADO ──
        video_path = settings.MEDIA_ROOT / "videos" / "guerreros.mp4"
        if video_path.exists():
            VideoDestacado.objects.create(
                titulo="Así vive la Academia Guerreros CF",
                descripcion="Un vistazo a nuestros entrenamientos, partidos y celebraciones.",
                video="videos/guerreros.mp4",
                portada=self._rel("evento1.jpg"),
                orden=0,
            )

        # ── 10. CONTACTO ──
        for i, (icono, titulo, detalle) in enumerate([
            ("📱", "WhatsApp / Teléfono", "241-105-5982 — Profesor Santos"),
            ("📍", "Ubicación", "San Dionisio Yauhquemehcan, Unidad Deportiva, Tlaxcala"),
            ("🕐", "Horario de atención", "Lunes a Viernes 4:00–6:00 PM · Domingos todo el día"),
            ("⚽", "Categorías disponibles", "7–18 años · Libre Varonil · Libre Femenil"),
        ]):
            InfoContacto.objects.create(icono=icono, titulo=titulo, detalle=detalle, orden=i)

        self.stdout.write(self.style.SUCCESS(
            f"Sitio sembrado correctamente: {GaleriaImagen.objects.count()} fotos en galería, "
            f"{HeroSlide.objects.count()} en el inicio, {FilosofiaSlide.objects.count()} en filosofía, "
            f"{MaterialSlide.objects.count()} en materiales de entrenamiento, "
            f"{EquipoFinalista.objects.count()} equipos finalistas, {Publicidad.objects.count()} anuncios, "
            f"{EventoSlide.objects.count()} eventos, {Noticia.objects.count()} noticias."
        ))

    # ── helpers ──
    @staticmethod
    def _rel(name):
        return f"img/{name}"

    def _create_img(self, Model, name, **extra):
        obj = Model(**extra)
        obj.imagen = self._rel(name)
        obj.save()
        return obj
