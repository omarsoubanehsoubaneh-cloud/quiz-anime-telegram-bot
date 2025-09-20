import os
import json
import random
import time
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging

# Configuration des logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(name)

# Token depuis les variables d'environnement (sécurisé)
BOT_TOKEN = os.getenv('BOT_TOKEN', '8439647366:AAFGwj_7vWMsmpgwJp-hsVFh6x3vJhqJm28')

# Questions du quiz avec images et audio - Collection mondiale d'animes
QUESTIONS = [
    # === QUESTIONS TEXTE - ANIMES DU MONDE ENTIER ===
    {
        "type": "text",
        "question": "Dans quel pays se déroule l'action de 'Spirited Away' (Le Voyage de Chihiro) ?",
        "options": ["Japon", "Chine", "Corée du Sud", "Monde imaginaire"],
        "correct": 0,
        "difficulty": "medium",
        "anime": "Spirited Away"
    },
    {
        "type": "text", 
        "question": "Quel est le vrai nom du personnage principal de Death Note ?",
        "options": ["Light Yagami", "Kira", "L Lawliet", "Ryuk"],
        "correct": 0,
        "difficulty": "easy",
        "anime": "Death Note"
    },
    {
        "type": "text",
        "question": "Dans Steins;Gate, comment s'appelle la machine à voyager dans le temps ?",
        "options": ["Phone Microwave", "Time Machine", "SERN Device", "D-Mail"],
        "correct": 0,
        "difficulty": "hard",
        "anime": "Steins;Gate"
    },
    {
        "type": "text",
        "question": "Quel est le pouvoir principal d'Izuku Midoriya dans My Hero Academia ?",
        "options": ["Explosion", "One For All", "Half-Cold Half-Hot", "Creation"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "My Hero Academia"
    },
    {
        "type": "text",
        "question": "Dans quel anime trouve-t-on la technique 'Jajanken' ?",
        "options": ["Naruto", "Hunter x Hunter", "Dragon Ball", "Yu Yu Hakusho"],
        "correct": 1,
        "difficulty": "hard",
        "anime": "Hunter x Hunter"
    },
    {
        "type": "text",
        "question": "Comment s'appelle l'organisation secrète dans Psycho-Pass ?",
        "options": ["Sibyl System", "MWPSB", "Enforcers", "Inspectors"],
        "correct": 0,
        "difficulty": "hard",
        "anime": "Psycho-Pass"
    },
    {
        "type": "text",
        "question": "Dans Tokyo Revengers, quel est le nom du gang principal ?",
        "options": ["Black Dragons", "Tokyo Manji Gang", "Brahman", "Tenjiku"],
        "correct": 1,
        "difficulty": "medium",
        "anime": "Tokyo Revengers"
    },
    
    # === QUESTIONS IMAGES - PERSONNAGES ICONIQUES ===
    {
        "type": "image",
        "question": "Qui est ce personnage aux cheveux blonds et aux cicatrices sur les joues ?",
        "image_url": "https://static.wikia.nocookie.net/naruto/images/d/dd/Naruto_Part_II.png/revision/latest?cb=20240127012920",
        "options": ["Sasuke Uchiha", "Naruto Uzumaki", "Minato Namikaze", "Boruto Uzumaki"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "Naruto"
    },
    {
        "type": "image", 
        "question": "Reconnaissez-vous ce personnage avec son chapeau de paille iconique ?",
        "image_url": "https://static.wikia.nocookie.net/onepiece/images/6/6d/Monkey_D._Luffy_Anime_Post_Timeskip_Infobox.png/revision/latest?cb=20200429191518",
        "options": ["Ace", "Sabo", "Monkey D. Luffy", "Shanks"],
        "correct": 2,
        "difficulty": "easy",
        "anime": "One Piece"
    },
    {
        "type": "image",
        "question": "Qui est ce personnage aux yeux verts déterminés ?",
        "image_url": "https://static.wikia.nocookie.net/shingekinokyojin/images/a/a1/Eren_Jaeger_%28Anime%29_character_image_%28The_Final_Season%29.png/revision/latest?cb=20210110153809",
        "options": ["Armin Arlert", "Eren Jaeger", "Levi Ackerman", "Jean Kirstein"],
        "correct": 1,
        "difficulty": "easy",
      "anime": "Attack on Titan"
    },
    {
        "type": "image",
        "question": "Qui est ce jeune héros avec ses cicatrices caractéristiques ?",
        "image_url": "https://static.wikia.nocookie.net/kimetsu-no-yaiba/images/4/44/Tanjiro_anime_design.png/revision/latest?cb=20190616233247",
        "options": ["Zenitsu Agatsuma", "Tanjiro Kamado", "Inosuke Hashibira", "Giyu Tomioka"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "Demon Slayer"
    },
    {
        "type": "image",
        "question": "Reconnaissez-vous ce personnage aux cheveux verts bouclés ?",
        "image_url": "https://static.wikia.nocookie.net/bokunoheroacademia/images/5/5f/Izuku_Midoriya_Anime_Action_Shot.png/revision/latest?cb=20190721140812",
        "options": ["Katsuki Bakugo", "Shoto Todoroki", "Izuku Midoriya", "Tenya Iida"],
        "correct": 2,
        "difficulty": "medium",
        "anime": "My Hero Academia"
    },
    {
        "type": "image",
        "question": "Qui est ce personnage mystérieux avec un carnet noir ?",
        "image_url": "https://static.wikia.nocookie.net/deathnote/images/4/42/Light_Yagami.png/revision/latest?cb=20120814123001",
        "options": ["L Lawliet", "Light Yagami", "Near", "Mello"],
        "correct": 1,
        "difficulty": "medium",
        "anime": "Death Note"
    },
    {
        "type": "image",
        "question": "Reconnaissez-vous ce Saiyan légendaire ?",
        "image_url": "https://static.wikia.nocookie.net/dragonball/images/5/5b/Goku_DBS_Broly.png/revision/latest?cb=20181215161234",
        "options": ["Vegeta", "Gohan", "Goku", "Trunks"],
        "correct": 2,
        "difficulty": "easy",
        "anime": "Dragon Ball"
    },
    {
        "type": "image",
        "question": "Qui est ce personnage avec sa transformation de ghoul ?",
        "image_url": "https://static.wikia.nocookie.net/tokyoghoul/images/c/cd/Ken_Kaneki_%28Anime%29.png/revision/latest?cb=20140802094728",
        "options": ["Touka Kirishima", "Ken Kaneki", "Ayato Kirishima", "Uta"],
        "correct": 1,
        "difficulty": "medium",
        "anime": "Tokyo Ghoul"
    },
    
    # === QUESTIONS AUDIO - OPENINGS LÉGENDAIRES ===
    {
        "type": "audio",
        "question": "De quel anime vient cet opening emblématique ? (Blue Bird)",
        "audio_url": "https://www.youtube.com/watch?v=aJRu5ltxXjc",
        "options": ["Naruto", "Naruto Shippuden", "Boruto", "Rock Lee"],
        "correct": 1,
        "difficulty": "medium",
        "anime": "Naruto Shippuden"
    },
    {
        "type": "audio",
        "question": "Quel anime a cet opening iconique ? (We Are!)",
        "audio_url": "https://www.youtube.com/watch?v=RSe8D2wfGKI",
        "options": ["Dragon Ball", "One Piece", "Fairy Tail", "Bleach"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "One Piece"
    },
    {
        "type": "audio",
        "question": "Reconnaissez-vous cet opening ? (Cha-La Head-Cha-La)",
        "audio_url": "https://www.youtube.com/watch?v=GHnfX1RmZX8",
        "options": ["Dragon Ball", "Dragon Ball Z", "Dragon Ball GT", "Dragon Ball Super"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "Dragon Ball Z"
    },
    {
        "type": "audio",
        "question": "De quel anime vient cette musique épique ? (Guren no Yumiya)",
        "audio_url": "https://www.youtube.com/watch?v=XMXgHfHxKVM",
        "options": ["Tokyo Ghoul", "Attack on Titan", "Parasyte", "Kabaneri"],
        "correct": 1,
        "difficulty": "medium",
        "anime": "Attack on Titan"
    },
    {
        "type": "audio",
        "question": "Quel anime a cet opening mystérieux ? (A Cruel Angel's Thesis)",
        "audio_url": "https://www.youtube.com/watch?v=nU21rCWkuJw",
        "options": ["Serial Experiments Lain", "Neon Genesis Evangelion", "Akira", "Ghost in the Shell"],
        "correct": 1,
        "difficulty": "hard",
        "anime": "Neon Genesis Evangelion"
    },
    {
        "type": "audio",
        "question": "De quel anime récent vient cet opening ? (Gurenge)",
      "audio_url": "https://www.youtube.com/watch?v=pmanD_s7G1o",
        "options": ["Jujutsu Kaisen", "Demon Slayer", "Chainsaw Man", "Tokyo Revengers"],
        "correct": 1,
        "difficulty": "easy",
        "anime": "Demon Slayer"
    },
    {
        "type": "audio",
        "question": "Reconnaissez-vous cet opening de jazz ? (Tank!)",
        "audio_url": "https://www.youtube.com/watch?v=NRI_8PUXx2A",
        "options": ["Samurai Champloo", "Cowboy Bebop", "Black Lagoon", "Baccano!"],
        "correct": 1,
        "difficulty": "hard",
        "anime": "Cowboy Bebop"
    },
    {
        "type": "audio", 
        "question": "De quel anime vient cet opening récent ? (Kaikai Kitan)",
        "audio_url": "https://www.youtube.com/watch?v=6riDJMI-Y8U",
        "options": ["Chainsaw Man", "Jujutsu Kaisen", "Hell's Paradise", "Tokyo Revengers"],
        "correct": 1,
        "difficulty": "medium",
        "anime": "Jujutsu Kaisen"
    },
    {
        "type": "audio",
        "question": "Quel anime a cet opening entraînant ? (Again)",
        "audio_url": "https://www.youtube.com/watch?v=2uq34TeWEdQ",
        "options": ["Fullmetal Alchemist", "Fullmetal Alchemist: Brotherhood", "Soul Eater", "D.Gray-man"],
        "correct": 1,
        "difficulty": "medium",
        "anime": "Fullmetal Alchemist: Brotherhood"
    },
    {
        "type": "audio",
        "question": "De quel anime vient cette mélodie nostalgique ? (Butter-Fly)",
        "audio_url": "https://www.youtube.com/watch?v=7cSB1IZU_8U",
        "options": ["Pokemon", "Digimon Adventure", "Yu-Gi-Oh!", "Monster Rancher"],
        "correct": 1,
        "difficulty": "hard",
        "anime": "Digimon Adventure"
    },
    
    # === QUESTIONS MIXTES - CULTURE OTAKU MONDIALE ===
    {
        "type": "text",
        "question": "Quel studio a produit 'Your Name' (Kimi no Na wa) ?",
        "options": ["Studio Ghibli", "Madhouse", "CoMix Wave Films", "Toei Animation"],
        "correct": 2,
        "difficulty": "hard",
        "anime": "Your Name"
    },
    {
        "type": "text",
        "question": "Dans quel anime trouve-t-on la technique de respiration 'Hinokami Kagura' ?",
        "options": ["Demon Slayer", "Bleach", "Naruto", "Black Clover"],
        "correct": 0,
        "difficulty": "medium",
        "anime": "Demon Slayer"
    },
    {
        "type": "text",
        "question": "Quel est le nom de l'école dans 'My Hero Academia' ?",
        "options": ["U.A. High School", "Shiketsu High", "Ketsubutsu Academy", "Isamu Academy"],
        "correct": 0,
        "difficulty": "easy",
        "anime": "My Hero Academia"
    }
]

# Sessions utilisateurs
user_sessions = {}

class AnimeQuizBot:
    def init(self, token):
        self.app = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Configure les handlers du bot"""
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("quiz", self.start_quiz))
        self.app.add_handler(CommandHandler("score", self.show_score))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CallbackQueryHandler(self.handle_answer))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /start"""
        welcome_text = """
🎌 Bienvenue dans le Quiz Anime Universel ! 🎌

Je suis votre bot quiz spécialisé dans l'univers de l'anime !

🎯 Fonctionnalités :
- 7 questions par quiz (texte, images, openings)
- Animes du monde entier (classiques & récents)
- Questions chronométrées (10 secondes)
- Système de points avec bonus vitesse

📋 Commandes :
- /quiz - Commencer un nouveau quiz
- /score - Voir votre score actuel
- /help - Afficher l'aide détaillée

🏆 Système de points :
- Bonne réponse : 10 points
- Bonus vitesse : +5 points (< 5 secondes)
      Prêt à tester vos connaissances otaku ? Tapez /quiz ! 🚀
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def start_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Démarre un nouveau quiz"""
        user_id = update.effective_user.id
        
        # Sélectionner 7 questions aléatoires pour plus de variété
        selected_questions = random.sample(QUESTIONS, min(7, len(QUESTIONS)))
        
        user_sessions[user_id] = {
            'questions': selected_questions,
            'current_question': 0,
            'score': 0,
            'start_time': time.time(),
            'question_start_time': time.time()
        }
        
        username = update.effective_user.first_name or "Otaku"
        await update.message.reply_text(
            f"🎯 Quiz démarré pour {username} !**\n\n🌍 7 questions d'animes du monde entier !\n⏰ 10 secondes par question\n🖼 Images, 🎵 openings & 📝 culture otaku !\n\nPremière question arrive...", 
            parse_mode='Markdown'
        )
        await asyncio.sleep(1)
        await self.send_question(update, context, user_id)
    
    async def send_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """Envoie une question à l'utilisateur"""
        session = user_sessions.get(user_id)
        if not session:
            return
        
        current_q_index = session['current_question']
        if current_q_index >= len(session['questions']):
            await self.end_quiz(update, context, user_id)
            return
        
        question = session['questions'][current_q_index]
        session['question_start_time'] = time.time()
        
        # Créer le texte de la question
        difficulty_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}
        difficulty = question.get('difficulty', 'medium')
        
        question_text = f"**Question {current_q_index + 1}/7 ⏱️\n\n"
        question_text += f"🎯 {question['question']}\n\n"
        question_text += f"📚 Anime: {question['anime']}\n"
        question_text += f"💎 Difficulté: {difficulty_emoji[difficulty]} {difficulty.capitalize()}\n"
        question_text += f"⏰ Temps: 10 secondes"
        
        # Créer les boutons de réponse
        keyboard = []
        for i, option in enumerate(question['options']):
            keyboard.append([InlineKeyboardButton(f"{chr(65+i)}. {option}", callback_data=f"answer_{i}")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Envoyer selon le type de question
        question_type = question.get('type', 'text')
        
        if question_type == 'image' and 'image_url' in question:
            try:
                await context.bot.send_photo(
                    chat_id=user_id,
                    photo=question['image_url'],
                    caption=question_text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Erreur envoi image: {e}")
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"🖼 [Image non disponible]\n\n{question_text}",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        
        elif question_type == 'audio' and 'audio_url' in question:
            try:
                # Pour les openings YouTube, on utilise le lien direct
                if 'youtube.com' in question['audio_url'] or 'youtu.be' in question['audio_url']:
                    await context.bot.send_message(
                        chat_id=user_id,
                      text=f"🎵 Opening à identifier :**\n{question['audio_url']}\n\n{question_text}",
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )
                else:
                    await context.bot.send_audio(
                        chat_id=user_id,
                        audio=question['audio_url'],
                        caption=question_text,
                        reply_markup=reply_markup,
                        parse_mode='Markdown',
                        title="Opening Anime Quiz",
                        performer="Quiz Anime Bot"
                    )
            except Exception as e:
                logger.error(f"Erreur envoi audio: {e}")
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"🎵 **Opening : {question['audio_url']}\n\n{question_text}",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
        
        else:
            # Question texte normale
            await context.bot.send_message(
                chat_id=user_id,
                text=question_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        # Programmer le timeout à 10 secondes
        context.job_queue.run_once(
            self.question_timeout,
            when=10.0,  # 10 secondes au lieu de 30
            data={'user_id': user_id, 'question_index': current_q_index}
        )
    
    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Traite la réponse de l'utilisateur"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        session = user_sessions.get(user_id)
        
        if not session:
            await query.edit_message_text("❌ Session expirée. Tapez /quiz pour recommencer.")
            return
        
        # Extraire la réponse
        try:
            answer_index = int(query.data.split('_')[1])
        except (IndexError, ValueError):
            await query.edit_message_text("❌ Erreur dans la réponse. Tapez /quiz pour recommencer.")
            return
        
        current_q_index = session['current_question']
        question = session['questions'][current_q_index]
        
        # Calculer le temps de réponse
        response_time = time.time() - session['question_start_time']
        is_correct = answer_index == question['correct']
        
        # Calculer les points avec bonus vitesse ajusté pour 10 secondes
        points = 0
        if is_correct:
            points = 10
            if response_time < 5:  # Bonus vitesse pour réponse < 5 secondes (au lieu de 10)
                points += 5
        
        session['score'] += points
        
        # Créer le message de résultat
        if is_correct:
            result_text = "✅ Excellente réponse ! 🎉\n"
            if response_time < 5:  # Bonus vitesse ajusté
                result_text += f"⚡️ Bonus vitesse ! ({response_time:.1f}s)\n"
            else:
                result_text += f"⏰ Temps: {response_time:.1f}s\n"
        else:
            result_text = "❌ Dommage ! 😔\n"
            result_text += f"💡 La bonne réponse était: {question['options'][question['correct']]}**\n"
            result_text += f"⏰ Temps: {response_time:.1f}s\n"
        
        result_text += f"\n💰 **Points gagnés: +{points}\n"
        result_text += f"🏆 Score total: {session['score']} points\n"
        result_text += f"📊 Progression: {current_q_index + 1}/7"
        
        await query.edit_message_text(result_text, parse_mode='Markdown')
        
        # Question suivante
        session['current_question'] += 1
        await asyncio.sleep(3)  # Pause de 3 secondes
        await self.send_question(update, context, user_id)
    
    async def question_timeout(self, context: ContextTypes.DEFAULT_TYPE):
        """Gère l'expiration d'une question"""
        job_data = context.job.data
      user_id = job_data['user_id']
        question_index = job_data['question_index']
        
        session = user_sessions.get(user_id)
        if not session or session['current_question'] != question_index:
            return
        
        # Timeout
        question = session['questions'][question_index]
        timeout_text = f"⏰ Temps écoulé ! ⏰\n\n"
        timeout_text += f"💡 La bonne réponse était: {question['options'][question['correct']]}**\n"
        timeout_text += f"🏆 Score actuel: {session['score']} points"
        
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=timeout_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Erreur timeout: {e}")
        
        session['current_question'] += 1
        await asyncio.sleep(2)
        
        # Question suivante
        fake_update = type('obj', (object,), {
            'effective_chat': type('obj', (object,), {'id': user_id}),
            'effective_user': type('obj', (object,), {'id': user_id})
        })()
        
        await self.send_question(fake_update, context, user_id)
    
    async def end_quiz(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
        """Termine le quiz et affiche le score final"""
        session = user_sessions.get(user_id)
        if not session:
            return
        
        total_time = time.time() - session['start_time']
        score = session['score']
        max_score = len(session['questions']) * 15  # 10 + 5 bonus max par question
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        
        # Déterminer le rang selon le pourcentage
        if percentage >= 90:
            rank = "🏆 **Maître Otaku Légendaire"
            emoji = "👑"
        elif percentage >= 80:
            rank = "🥇 Expert Anime"
            emoji = "⭐️"
        elif percentage >= 60:
            rank = "🥈 Fan Confirmé"
            emoji = "🎖"
        elif percentage >= 40:
            rank = "🥉 Amateur Éclairé"
            emoji = "📚"
        else:
            rank = "🎌 Apprenti Otaku"
            emoji = "🌱"
        
        username = update.effective_user.first_name or "Otaku"
        
        final_text = f"""
🎊 Quiz terminé, {username} ! 🎊

{emoji} RÉSULTATS FINAUX {emoji}

🏆 Score: {score}/{max_score} points
📈 Réussite: {percentage:.1f}%
⏱️ Temps total: {total_time/60:.1f} minutes
🎭 Rang obtenu: {rank}

📊 Statistiques détaillées:
- Questions traitées: {len(session['questions'])}
- Temps moyen/question: {total_time/len(session['questions']):.1f}s
- Efficacité: {"🔥 Excellent" if percentage >= 80 else "👍 Bien" if percentage >= 60 else "💪 À améliorer"}

🎮 Prêt pour un nouveau défi ? Tapez /quiz !
📚 Besoin d'aide ? Tapez /help

Merci d'avoir joué ! 🎌✨
        """
        
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text=final_text,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Erreur fin de quiz: {e}")
        
        # Nettoyer la session
        if user_id in user_sessions:
            del user_sessions[user_id]
    
    async def show_score(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Affiche le score actuel si un quiz est en cours"""
        user_id = update.effective_user.id
        session = user_sessions.get(user_id)
        
        if not session:
            await update.message.reply_text(
                "❌ Aucun quiz en cours !**\n\n🎯 Tapez /quiz pour commencer votre aventure anime ! 🎌", 
                parse_mode='Markdown'
            )
            return
        
        current_q = session['current_question']
        total_q = len(session['questions'])
        score = session['score']
        elapsed_time = (time.time() - session['start_time']) / 60
        
        status_text = f"""
📊 **Quiz en cours 📊
      🎯 Progression: {current_q}/{total_q} questions
🏆 Score actuel: {score} points
⏱️ Temps écoulé: {elapsed_time:.1f} minutes
🔥 Statut: {"🚀 En feu !" if score >= current_q * 10 else "💪 Continue !"}

⚡️ Prochaine question arrive...
        """
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Commande /help"""
        help_text = """
🆘 Guide du Quiz Anime 🆘

🎮 Comment jouer :
1️⃣ Tapez /quiz pour commencer
2️⃣ Répondez aux 7 questions via les boutons
3️⃣ Chaque question a 10 secondes
4️⃣ Gagnez des points et déverrouillez votre rang !

🏆 Système de points :
- ✅ Bonne réponse : 10 points
- ⚡️ Bonus vitesse : +5 points (< 5 secondes)
- ❌ Mauvaise réponse : 0 point

🎭 Types de questions :
- 📝 Texte - Culture otaku mondiale
- 🖼 Images - Personnages iconiques
- 🎵 Openings - Musiques légendaires d'anime

🌍 Animes inclus :
- Classiques : Naruto, One Piece, Dragon Ball, Death Note
- Modernes : Demon Slayer, Jujutsu Kaisen, Attack on Titan
- Cultes : Cowboy Bebop, Evangelion, Studio Ghibli
- Et bien plus !

🎭 Niveaux de difficulté :
- 🟢 Facile - Anime populaires (Naruto, One Piece...)
- 🟡 Moyen - Connaissances générales
- 🔴 Difficile - Pour les vrais experts !

🏅 Rangs disponibles :
- 👑 Maître Otaku Légendaire (90%+)
- ⭐️ Expert Anime (80%+)
- 🎖 Fan Confirmé (60%+)
- 📚 Amateur Éclairé (40%+)
- 🌱 Apprenti Otaku (<40%)

📋 Commandes utiles :
- /quiz - Nouveau quiz
- /score - Score actuel
- /start - Retour à l'accueil
- /help - Cette aide

🎌 Bon quiz et que le meilleur otaku gagne ! 🎌
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    def run(self):
        """Lance le bot"""
        logger.info("🤖 Quiz Anime Bot démarré sur Railway !")
        self.app.run_polling(drop_pending_updates=True)

if name == "main":
    bot = AnimeQuizBot(BOT_TOKEN)
    bot.run()
