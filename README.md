# Academia Guerreros CF Yauhquemehcan — sitio en Django

Sitio web completo de la Academia Guerreros CF convertido a **Django**, con
cada sección del sitio manejada desde su propio modelo editable en el panel
de administración: Inicio (carrusel), Noticias, Campeonas, Galería,
Filosofía, Eventos, Video, Academia y Contacto.

Incluye las **279 fotos** y el **video** que enviaste, ya colocados en su
lugar correspondiente (portada, noticias, campeonas, galería, carrusel de
filosofía, eventos y sección de video).

## 1. Instalación

```bash
# Crear entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## 2. Configurar variables de entorno (opcional pero recomendado)

```bash
cp .env.example .env
```

Abre `.env` y como mínimo cambia `SECRET_KEY` por algo único. Si vas a usar
Cloudinary (ver sección 6), pon ahí tus credenciales.

## 3. Preparar la base de datos

```bash
python manage.py makemigrations core
python manage.py migrate
```

## 4. Cargar todo el contenido (fotos, noticias, eventos, etc.)

Las fotos y el video ya están copiados dentro de `media/img/` y
`media/videos/`. Este comando crea automáticamente todos los registros en
la base de datos apuntando a esas fotos:

```bash
python manage.py seed_site
```

Puedes volver a ejecutarlo cuando quieras: primero borra el contenido
anterior y lo vuelve a crear desde cero (no borra los mensajes de
contacto que te dejen los visitantes).

## 5. Crear un usuario administrador

```bash
python manage.py createsuperuser
```

## 6. Cloudinary (guardar las fotos en la nube, opcional)

Por defecto las fotos que subas desde `/admin/` se guardan en la carpeta
`media/` del propio servidor. Eso funciona perfecto en tu computadora,
pero si más adelante subes el sitio a un hosting como **Render, Railway o
Heroku**, ese disco se borra cada vez que el servidor reinicia y perderías
las fotos nuevas que suba el administrador. Cloudinary resuelve esto
guardándolas en la nube de forma permanente y gratuita (plan free
generoso, de sobra para un sitio como este).

**Pasos:**
1. Crea una cuenta gratis en https://cloudinary.com/users/register/free
2. En tu **Dashboard** de Cloudinary verás 3 datos: *Cloud name*, *API Key*
   y *API Secret*.
3. Pégalos en tu archivo `.env`:
   ```
   CLOUDINARY_CLOUD_NAME=tu_cloud_name
   CLOUDINARY_API_KEY=tu_api_key
   CLOUDINARY_API_SECRET=tu_api_secret
   ```
4. Reinicia el servidor (`python manage.py runserver`). A partir de ese
   momento, **toda foto nueva que subas desde el admin** se guarda
   automáticamente en Cloudinary.

Si dejas esas 3 variables vacías, el sitio sigue funcionando exactamente
igual que antes (guardando todo en `media/` local) — Cloudinary es
100% opcional y no rompe nada si no lo usas.

> Nota: las fotos que ya están precargadas por `seed_site` seguirán
> sirviéndose desde `media/img/` local, ya que ese comando lee archivos
> directamente del disco. Cloudinary solo aplica a las fotos que subas
> manualmente desde el panel de administración después de configurarlo.

## 7. Ejecutar el sitio

```bash
python manage.py runserver
```

- Sitio público: http://127.0.0.1:8000/
- Panel de administración: http://127.0.0.1:8000/admin/

## Editar el contenido

Todo el contenido del sitio se administra desde `/admin/` sin tocar
código: puedes agregar/quitar fotos de la galería, cambiar noticias,
logros, tarjetas de la academia, datos de contacto, subir un nuevo video,
etc. Cada sección aparece numerada en el menú del admin en el mismo orden
en que aparece en la página (1. Inicio, 2. Noticias, 3. Campeonas...).

Los mensajes que la gente envíe desde el formulario de contacto se
guardan en **11. Mensajes de contacto** dentro del admin, y además se
abren automáticamente por WhatsApp al número 241-105-5982.

## Estructura del proyecto

```
guerreros_django/       Configuración del proyecto (settings, urls)
core/                   App principal
  models.py             Un modelo por sección del sitio
  admin.py               Panel de administración con miniaturas
  views.py               Vista que arma la página con todo el contenido
  management/commands/seed_site.py   Carga inicial de contenido
  static/core/           CSS y JS del sitio
  templates/core/        Plantilla HTML (index.html)
media/img/               Las 279 fotos que enviaste
media/videos/            El video guerreros.mp4
```

## Publicar el sitio para que lo vea el público

Recomiendo **Render** (https://render.com): tiene plan gratis, no pide
tarjeta de crédito, y detecta Django automáticamente. Así se hace, paso a
paso:

### Paso 0 — Cosas que debes preparar antes

1. **Cuenta de Cloudinary** (para que las fotos no se borren) — ver
   sección 6 de arriba. Configúrala **antes** de sembrar el contenido en
   producción, para que las fotos se suban directo a Cloudinary.
2. **Tu video pesa ~180 MB.** Ni GitHub (límite 100 MB) ni el plan
   gratuito de Cloudinary (límite 100 MB) lo aceptan tal cual. La
   solución más simple y **gratis**: sube el video a YouTube (puede ser
   "oculto" — no listado — si no quieres que aparezca en búsquedas de
   YouTube, pero sigue siendo visible para quien entre a tu sitio) y
   luego pega el link en el campo **"Link de YouTube"** del video en el
   admin, dejando vacío el campo de archivo. El sitio ya está preparado
   para mostrarlo así. El `.gitignore` ya excluye el .mp4 para que no
   truene la subida a GitHub.

### Paso 1 — Subir el proyecto a GitHub

```bash
cd guerreros_django
git init
git add .
git commit -m "Sitio Guerreros CF"
```
Crea un repositorio nuevo en https://github.com/new (puede ser privado) y
sigue las instrucciones que te da GitHub para conectarlo y subir tu
código (`git remote add origin ...` y `git push`).

> El `.gitignore` ya excluye `.env`, `db.sqlite3` y el video pesado, así
> que no se suben por accidente.

### Paso 2 — Crear la base de datos en Render

1. En tu Dashboard de Render → **New +** → **PostgreSQL**.
2. Dale un nombre (ej. `guerreros-db`) y elige el plan **Free**.
3. Cuando esté creada, copia el valor **"Internal Database URL"** (lo vas
   a necesitar en el paso 3).

> El plan gratis de Postgres en Render caduca después de un tiempo (te
> avisan antes) y hay que renovarlo o pasar al plan pagado (~$7/mes) si
> quieres que el sitio siga funcionando sin interrupciones a largo plazo.

### Paso 3 — Crear el Web Service

1. Dashboard de Render → **New +** → **Web Service** → conecta tu
   repositorio de GitHub.
2. Configura:
   - **Build Command:** `bash build.sh`
   - **Start Command:** `gunicorn guerreros_django.wsgi:application`
   - **Plan:** Free (o Starter $7/mes si no quieres que el sitio "duerma"
     tras 15 minutos sin visitas — en el plan gratis, la primera visita
     después de un rato tarda ~30 segundos en cargar).
3. En la pestaña **Environment**, agrega estas variables:
   | Variable | Valor |
   |---|---|
   | `SECRET_KEY` | una clave larga y aleatoria (puedes generarla en https://djecrety.ir/) |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `tu-sitio.onrender.com` (Render te da este dominio) |
   | `CSRF_TRUSTED_ORIGINS` | `https://tu-sitio.onrender.com` |
   | `DATABASE_URL` | pega aquí el "Internal Database URL" del paso 2 |
   | `CLOUDINARY_CLOUD_NAME` | el de tu cuenta Cloudinary |
   | `CLOUDINARY_API_KEY` | el de tu cuenta Cloudinary |
   | `CLOUDINARY_API_SECRET` | el de tu cuenta Cloudinary |
4. Dale **Create Web Service**. Render instala todo, corre `build.sh`
   (que instala dependencias, junta los estáticos y aplica las
   migraciones) y levanta el sitio.

### Paso 4 — Cargar el contenido y crear tu usuario admin

Con el servicio ya desplegado, abre su **Shell** (pestaña "Shell" en el
dashboard de Render) y corre:

```bash
python manage.py seed_site
python manage.py createsuperuser
```

Como en ese momento ya tienes Cloudinary configurado, `seed_site` sube
las fotos directamente a la nube — no dependen del disco de Render.

### Paso 5 — ¡Listo!

Tu sitio ya es público en `https://tu-sitio.onrender.com`. Si tienes un
dominio propio (ej. `guerreroscf.mx`), en Render → tu servicio →
**Settings → Custom Domains** puedes conectarlo (te da los registros DNS
que debes configurar donde compraste el dominio).

Cada vez que hagas `git push` con cambios de código, Render vuelve a
desplegar el sitio automáticamente. Los cambios de contenido (fotos,
noticias, etc.) se hacen siempre desde `/admin/`, sin tocar código ni
volver a hacer `push`.
"# guerreros-cf" 
