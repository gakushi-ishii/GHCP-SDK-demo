import chalk from 'chalk';

/**
 * ロガーユーティリティ
 * デモアプリでの出力を見やすくするためのヘルパー
 */
export class Logger {
  static info(message: string): void {
    console.log(chalk.blue('ℹ'), message);
  }

  static success(message: string): void {
    console.log(chalk.green('✓'), message);
  }

  static error(message: string): void {
    console.log(chalk.red('✗'), message);
  }

  static warning(message: string): void {
    console.log(chalk.yellow('⚠'), message);
  }

  static header(message: string): void {
    console.log('\n' + chalk.bold.cyan('═'.repeat(60)));
    console.log(chalk.bold.cyan(message));
    console.log(chalk.bold.cyan('═'.repeat(60)) + '\n');
  }

  static section(message: string): void {
    console.log('\n' + chalk.bold.white(message));
    console.log(chalk.gray('─'.repeat(60)));
  }

  static code(code: string, language: string = ''): void {
    console.log(chalk.gray('\n```' + language));
    console.log(code);
    console.log(chalk.gray('```\n'));
  }

  static result(label: string, value: string): void {
    console.log(chalk.cyan(label + ':'), chalk.white(value));
  }
}
