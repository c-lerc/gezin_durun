// @ts-nocheck
import crypto from 'crypto';
import fs from 'fs';
import path from 'path';

export default {
  /**
   * An asynchronous register function that runs before
   * your application is initialized.
   *
   * This gives you an opportunity to extend code.
   */
  register(/* { strapi } */) {},

  /**
   * An asynchronous bootstrap function that runs before
   * your application gets started.
   *
   * This gives you an opportunity to set up your data model,
   * run jobs, or perform some special logic.
   */
  async bootstrap({ strapi }) {
    try {
      // 1. Setup Locales for i18n
      const localeService = strapi.plugin('i18n').service('locales');
      if (localeService) {
        const existingLocales = await localeService.find();
        
        let hasTR = existingLocales.some(l => l.code === 'tr');
        let hasEN = existingLocales.some(l => l.code === 'en');
        
        if (!hasTR) {
          await localeService.create({ name: 'Turkish', code: 'tr' });
          console.log('Turkish (tr) locale created.');
        }
        if (!hasEN) {
          await localeService.create({ name: 'English', code: 'en' });
          console.log('English (en) locale created.');
        }

        // Try to set TR as default
        try {
          const trLocale = await localeService.findByCode('tr');
          if (trLocale && !trLocale.isDefault) {
             await localeService.setDefaultLocale({ code: 'tr' });
             console.log('Set Turkish as default locale.');
          }
        } catch (e) {
          console.log('Could not set default locale:', e.message);
        }
      }

      // 2. Generate Full-Access API Token for Python & Streamlit
      const tokenService = strapi.service('admin::api-token');
      if (tokenService) {
        // Safe way to check existing tokens without causing service errors
        const existingTokens = await strapi.db.query('admin::api-token').findMany();
        let pythonToken = existingTokens.find(t => t.name === 'PythonEngineToken');
        
        if (!pythonToken) {
          try {
            const token = await tokenService.create({
              name: 'PythonEngineToken',
              description: 'Token for Python automation and Streamlit frontend',
              type: 'full-access',
              lifespan: null
            });
            
            const pythonEnvPath = path.join(process.cwd(), '../python_engine/.env');
            const frontendEnvPath = path.join(process.cwd(), '../frontend/.env');
            
            fs.mkdirSync(path.dirname(pythonEnvPath), { recursive: true });
            fs.mkdirSync(path.dirname(frontendEnvPath), { recursive: true });
            
            // In Strapi v4/v5, the clear-text token is returned as accessKey
            const accessKey = token.accessKey || token.token; 
            if (accessKey) {
                const envContent = `STRAPI_API_TOKEN=${accessKey}\nSTRAPI_URL=http://localhost:1337\n`;
                fs.writeFileSync(pythonEnvPath, envContent);
                fs.writeFileSync(frontendEnvPath, envContent);
                console.log('API Token created and saved to python_engine and frontend .env files.');
            } else {
                console.log('Token created but accessKey could not be read.');
            }
          } catch (e) {
            console.log('Error creating token:', e.message);
          }
        } else {
          console.log('PythonEngineToken already exists.');
        }
      }
      // 3. Force-publish all cities and places
      try {
        await strapi.db.query('api::city.city').updateMany({
          where: { publishedAt: null },
          data: { publishedAt: new Date() }
        });
        await strapi.db.query('api::place.place').updateMany({
          where: { publishedAt: null },
          data: { publishedAt: new Date() }
        });
        console.log('Force published all draft cities and places.');
      } catch (e) {
        console.log('Error publishing drafts:', e.message);
      }
      // 4. Grant Public Read Permissions
      try {
        const publicRole = await strapi.db.query('plugin::users-permissions.role').findOne({ where: { type: 'public' } });
        if (publicRole) {
          const actions = ['api::city.city.find', 'api::place.place.find'];
          for (const action of actions) {
            const existing = await strapi.db.query('plugin::users-permissions.permission').findOne({ where: { action, role: publicRole.id }});
            if (!existing) {
              await strapi.db.query('plugin::users-permissions.permission').create({
                data: { action, role: publicRole.id }
              });
            }
          }
          console.log('Granted public read access to cities and places.');
        }
      } catch (e) {
        console.log('Error granting public access:', e.message);
      }
    } catch (error) {
      console.error('Error during bootstrap:', error);
    }
  },
};
