const { Client, GatewayIntentBits, Partials, EmbedBuilder } = require('discord.js');
require('dotenv').config();

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.GuildMessageReactions,
    GatewayIntentBits.GuildMembers,
  ],
  partials: [Partials.Message, Partials.Channel, Partials.Reaction],
});

// Reemplaza esto con el ID del mensaje que creará el comando !setup-autoroles
const TARGET_MESSAGE_ID = 'ID_DEL_MENSAJE_AQUI';

// Mapeo completo con los 20 países de la imagen
// Reemplaza 'ID_ROL_...' por el ID real de cada rol en tu Discord
const countryRoles = {
  '🇨🇴': 'ID_ROL_COLOMBIA',
  '🇲🇽': 'ID_ROL_MEXICO',
  '🇪🇸': 'ID_ROL_ESPAÑA',
  '🇻🇪': 'ID_ROL_VENEZUELA',
  '🇵🇷': 'ID_ROL_PUERTO_RICO',
  '🇪🇨': 'ID_ROL_ECUADOR',
  '🇦🇷': 'ID_ROL_ARGENTINA',
  '🇨🇱': 'ID_ROL_CHILE',
  '🇧🇴': 'ID_ROL_BOLIVIA',
  '🇬🇹': 'ID_ROL_GUATEMALA',
  '🇸🇻': 'ID_ROL_EL_SALVADOR',
  '🇭🇳': 'ID_ROL_HONDURAS',
  '🇳🇮': 'ID_ROL_NICARAGUA',
  '🇨🇷': 'ID_ROL_COSTA_RICA',
  '🇵🇦': 'ID_ROL_PANAMA',
  '🇨🇺': 'ID_ROL_CUBA',
  '🇩🇴': 'ID_ROL_REPUBLICA_DOMINICANA',
  '🇵🇪': 'ID_ROL_PERU',
  '🇵🇾': 'ID_ROL_PARAGUAY',
  '🇺🇾': 'ID_ROL_URUGUAY'
};

client.once('ready', () => {
  console.log(`Dark-bot encendido exitosamente como ${client.user.tag}`);
});

// Comando para publicar el mensaje del sistema de autoroles
client.on('messageCreate', async (message) => {
  // Reemplaza TU_ID_DE_DISCORD por tu ID de usuario de Discord
  if (message.content === '!setup-roles' && message.author.id === 'TU_ID_DE_DISCORD') {
    const embed = new EmbedBuilder()
      .setColor('#800000')
      .setTitle('🧸 | ¡ELIGE TU PAÍS!')
      .setDescription(
        '🇨🇴 | **REACCIONA A ESTE MENSAJE CON LA BANDERA DE TU PAÍS**\n\n' +
        '1. **Solo se puede seleccionar un país.**\n' +
        '2. **Si te equivocas** y tienes que cambiar de país; primero **quita la reacción y luego vuelve a reaccionar** al país que deseas.\n' +
        '3. Evita usar todos los emojis y así evitas bugs. Y listo, **disfruta del server con tu nuevo rol.** 👨‍💻'
      )
      .setFooter({ 
        text: 'En caso tengas dudas o reportes con algún bug, no dudes en abrir un ticket. | Dark-bot',
        iconURL: client.user.displayAvatarURL()
      });

    const sentMessage = await message.channel.send({ embeds: [embed] });

    for (const emoji of Object.keys(countryRoles)) {
      await sentMessage.react(emoji);
    }

    console.log(`Copia este ID y pégalo en TARGET_MESSAGE_ID: ${sentMessage.id}`);
  }
});

// Asignar rol al reaccionar
client.on('messageReactionAdd', async (reaction, user) => {
  if (user.bot) return;

  if (reaction.partial) {
    try { await reaction.fetch(); } catch (error) { return; }
  }

  if (reaction.message.id !== TARGET_MESSAGE_ID) return;

  const roleId = countryRoles[reaction.emoji.name];
  if (!roleId) return;

  const guild = reaction.message.guild;
  const member = await guild.members.fetch(user.id);

  try {
    for (const emoji in countryRoles) {
      const otherRoleId = countryRoles[emoji];
      if (otherRoleId !== roleId && member.roles.cache.has(otherRoleId)) {
        await member.roles.remove(otherRoleId);
      }
    }
    await member.roles.add(roleId);
  } catch (err) {
    console.error(`Error al añadir el rol: ${err}`);
  }
});

// Quitar rol al quitar la reacción
client.on('messageReactionRemove', async (reaction, user) => {
  if (user.bot) return;

  if (reaction.partial) {
    try { await reaction.fetch(); } catch (error) { return; }
  }

  if (reaction.message.id !== TARGET_MESSAGE_ID) return;

  const roleId = countryRoles[reaction.emoji.name];
  if (!roleId) return;

  const guild = reaction.message.guild;
  const member = await guild.members.fetch(user.id);

  try {
    await member.roles.remove(roleId);
  } catch (err) {
    console.error(`Error al remover el rol: ${err}`);
  }
});

client.login(process.env.DISCORD_TOKEN);

